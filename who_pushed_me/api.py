from __future__ import annotations

from functools import wraps
from io import BytesIO
from typing import Any, Callable

import psycopg
from flask import Blueprint, current_app, g, jsonify, request, send_file

from who_pushed_me.courses import OpenGolfAPI
from who_pushed_me.domain import DomainError, NotFound, PermissionDenied
from who_pushed_me.reporting import build_round_report_pdf
from who_pushed_me.store import RoundStore

api = Blueprint("api", __name__, url_prefix="/api")


def _store() -> RoundStore:
    configured = current_app.config.get("ROUND_STORE")
    if configured is not None:
        return configured
    return RoundStore(current_app.config.get("DATABASE_URL"))


def _course_provider():
    configured = current_app.config.get("COURSE_PROVIDER")
    if configured is not None:
        return configured
    return OpenGolfAPI(api_key=current_app.config.get("OPENGOLF_API_KEY") or None)


def _body() -> dict[str, Any]:
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise DomainError("request body must be a JSON object")
    return payload


def session_authenticated(view: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any):
        authorization = request.headers.get("Authorization", "").strip()
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token.strip():
            raise PermissionDenied("Bearer session token is required")
        g.session_token = token.strip()
        g.golfer = _store().authenticate_session(g.session_token)
        return view(*args, **kwargs)

    return wrapped


def authenticated(view: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any):
        authorization = request.headers.get("Authorization", "").strip()
        scheme, _, token = authorization.partition(" ")

        if scheme.lower() == "bearer" and token.strip():
            g.session_token = token.strip()
            g.golfer = _store().authenticate_session(g.session_token)
            return view(*args, **kwargs)

        key = request.headers.get("X-Recovery-Key", "")
        if key:
            g.golfer = _store().recover_golfer(key)
            return view(*args, **kwargs)

        raise PermissionDenied(
            "Bearer session token or X-Recovery-Key is required"
        )

    return wrapped


@api.errorhandler(PermissionDenied)
def permission_denied(error: PermissionDenied):
    return jsonify(error=str(error)), 403


@api.errorhandler(NotFound)
def not_found(error: NotFound):
    return jsonify(error=str(error)), 404


@api.errorhandler(DomainError)
def domain_error(error: DomainError):
    return jsonify(error=str(error)), 400


@api.errorhandler(psycopg.Error)
def database_error(error: psycopg.Error):
    current_app.logger.exception("database request failed")
    return jsonify(error="database request failed"), 503


@api.post("/auth/register")
def register_account():
    payload = _body()
    result = _store().register_account(
        username=payload.get("username"),
        password=payload.get("password"),
        display_name=payload.get("display_name"),
    )
    return jsonify(result), 201


@api.post("/auth/login")
def login_account():
    payload = _body()
    result = _store().login_account(
        username=payload.get("username"),
        password=payload.get("password"),
    )
    return jsonify(result)


@api.post("/auth/recover")
def recover_account():
    payload = _body()
    result = _store().recover_account_with_key(
        recovery_key=payload.get("recovery_key"),
        new_password=payload.get("new_password"),
    )
    return jsonify(result)


@api.get("/auth/me")
@session_authenticated
def auth_me():
    return jsonify(g.golfer)


@api.post("/auth/logout")
@session_authenticated
def auth_logout():
    return jsonify(_store().logout_session(g.session_token))


@api.post("/golfers")
def create_golfer():
    golfer = _store().create_golfer(_body().get("display_name"))
    return jsonify(golfer), 201


@api.post("/golfers/recover")
def recover_golfer():
    golfer = _store().recover_golfer(_body().get("recovery_key"))
    return jsonify(golfer)


@api.get("/courses/search")
@authenticated
def search_courses():
    query = request.args.get("q", "").strip()
    if len(query) < 2:
        raise DomainError("course search must be at least 2 characters")

    limit = min(max(request.args.get("limit", 10, type=int) or 10, 1), 25)
    cached = _store().search_cached_courses(query, limit=limit)

    results = [
        {
            "source": "cache",
            "course_id": row["id"],
            "external_course_id": row["external_course_id"],
            "name": row["name"],
        }
        for row in cached
    ]
    seen = {str(row["external_course_id"]) for row in cached}

    if len(results) < limit:
        try:
            provider_rows = _course_provider().search(
                query,
                limit=limit,
            )
        except Exception:
            current_app.logger.exception("course provider search failed")
            provider_rows = []

        for row in provider_rows:
            external_id = str(row.get("external_course_id") or "").strip()
            name = str(row.get("name") or "").strip()
            if not external_id or not name or external_id in seen:
                continue
            result = {
                "source": "provider",
                "external_course_id": external_id,
                "name": name,
            }
            for field in ("city", "state", "country"):
                if row.get(field):
                    result[field] = row[field]
            results.append(result)
            seen.add(external_id)
            if len(results) >= limit:
                break

    return jsonify(results=results)


@api.post("/courses/select")
@authenticated
def select_course():
    payload = _body()
    course_id = payload.get("course_id")
    if course_id:
        return jsonify(_store().get_cached_course(course_id))

    external_id = str(payload.get("external_course_id") or "").strip()
    if not external_id:
        raise DomainError("course_id or external_course_id is required")

    cached = _store().get_cached_course_by_external_id(external_id)
    if cached:
        return jsonify(cached)

    try:
        snapshot = _course_provider().fetch(external_id)
    except Exception as error:
        current_app.logger.exception("course provider fetch failed")
        raise DomainError("could not load that course right now") from error

    cached_id = _store().cache_course(snapshot)
    return jsonify(_store().get_cached_course(cached_id))


@api.get("/preferences")
@authenticated
def get_preferences():
    return jsonify(_store().get_content_preferences(g.golfer["id"]))


@api.patch("/preferences")
@authenticated
def update_preferences():
    return jsonify(
        _store().update_content_preferences(
            g.golfer["id"],
            _body(),
        )
    )


@api.post("/rounds")
@authenticated
def create_round():
    payload = _body()
    kwargs = {
        "mode": payload.get("mode"),
        "holes": payload.get("holes"),
        "course_id": payload.get("course_id"),
        "free_play_name": payload.get("free_play_name"),
        "tee_name": payload.get("tee_name"),
    }
    for key in (
        "start_hole",
        "end_hole",
        "course_hole_count",
        "par_tracking_enabled",
    ):
        if key in payload:
            kwargs[key] = payload.get(key)

    round_row = _store().create_round(
        g.golfer["id"],
        **kwargs,
    )
    return jsonify(round_row), 201


@api.post("/rounds/join")
@authenticated
def join_round():
    payload = _body()
    participant = _store().join_round(
        g.golfer["id"],
        code=payload.get("code"),
        role=payload.get("role"),
        tee_name=payload.get("tee_name"),
    )
    return jsonify(participant), 201


@api.get("/rounds/code/<code>")
@authenticated
def get_round(code: str):
    return jsonify(_store().get_round(g.golfer["id"], code))


@api.get("/rounds/<round_id>/report.pdf")
@authenticated
def download_round_report(round_id: str):
    round_row = _store().get_round(
        g.golfer["id"],
        round_id=round_id,
        event_limit=None,
    )
    if round_row["status"] != "completed":
        raise DomainError("final damage report is only available after the round is completed")

    preferences = _store().get_content_preferences(g.golfer["id"])
    pdf_bytes = build_round_report_pdf(
        round_row,
        preferences=preferences,
    )

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=(
            f"who-pushed-me-{round_row['active_code']}-final-damage-report.pdf"
        ),
        max_age=0,
    )


@api.patch("/rounds/<round_id>/tee")
@authenticated
def set_tee(round_id: str):
    return jsonify(
        _store().set_participant_tee(
            g.golfer["id"],
            round_id,
            _body().get("tee_name"),
        )
    )


@api.patch("/rounds/<round_id>/current-hole")
@authenticated
def set_current_hole(round_id: str):
    payload = _body()
    position = payload.get(
        "route_position",
        payload.get("hole"),
    )
    return jsonify(
        _store().set_current_hole(
            g.golfer["id"],
            round_id,
            position,
        )
    )


@api.patch("/rounds/<round_id>/status")
@authenticated
def set_status(round_id: str):
    return jsonify(_store().set_status(g.golfer["id"], round_id, _body().get("status")))


@api.put("/rounds/<round_id>/holes/<int:position>/par")
@api.put("/rounds/<round_id>/positions/<int:position>/par")
@authenticated
def set_par(round_id: str, position: int):
    return jsonify(
        _store().set_par(
            g.golfer["id"],
            round_id,
            position,
            _body().get("par"),
        )
    )


@api.put("/rounds/<round_id>/holes/<int:position>/score")
@api.put("/rounds/<round_id>/positions/<int:position>/score")
@authenticated
def set_score(round_id: str, position: int):
    payload = _body()
    return jsonify(
        _store().set_score(
            g.golfer["id"],
            round_id,
            position,
            payload.get("strokes"),
            player_participant_id=payload.get("player_participant_id"),
        )
    )


@api.put("/rounds/<round_id>/holes/<int:position>/contributions/<shot_type>")
@api.put("/rounds/<round_id>/positions/<int:position>/contributions/<shot_type>")
@authenticated
def set_contribution(
    round_id: str,
    position: int,
    shot_type: str,
):
    return jsonify(
        _store().set_scramble_contribution(
            g.golfer["id"],
            round_id,
            position,
            shot_type,
            _body().get("player_participant_id"),
        )
    )


@api.post("/rounds/<round_id>/score-events/<event_id>/responses")
@authenticated
def add_score_response(round_id: str, event_id: str):
    payload = _body()
    event = _store().add_score_response(
        g.golfer["id"],
        round_id,
        event_id,
        response_kind=payload.get("response_kind"),
        message=payload.get("message"),
        target_participant_id=payload.get("target_participant_id"),
    )
    return jsonify(event), 201


@api.post("/rounds/<round_id>/events")
@authenticated
def add_social_event(round_id: str):
    payload = _body()
    event = _store().add_social_event(
        g.golfer["id"],
        round_id,
        payload.get("type"),
        hole=payload.get("hole"),
        data=payload.get("data"),
    )
    return jsonify(event), 201
