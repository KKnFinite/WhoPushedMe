from __future__ import annotations

from functools import wraps
from typing import Any, Callable

import psycopg
from flask import Blueprint, current_app, g, jsonify, request

from who_pushed_me.domain import DomainError, NotFound, PermissionDenied
from who_pushed_me.store import RoundStore

api = Blueprint("api", __name__, url_prefix="/api")


def _store() -> RoundStore:
    configured = current_app.config.get("ROUND_STORE")
    if configured is not None:
        return configured
    return RoundStore(current_app.config.get("DATABASE_URL"))


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
        key = request.headers.get("X-Recovery-Key", "")
        if not key:
            raise PermissionDenied("X-Recovery-Key is required")
        g.golfer = _store().recover_golfer(key)
        return view(*args, **kwargs)

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
    round_row = _store().create_round(
        g.golfer["id"],
        mode=payload.get("mode"),
        holes=payload.get("holes"),
        course_id=payload.get("course_id"),
        free_play_name=payload.get("free_play_name"),
    )
    return jsonify(round_row), 201


@api.post("/rounds/join")
@authenticated
def join_round():
    payload = _body()
    participant = _store().join_round(
        g.golfer["id"], code=payload.get("code"), role=payload.get("role")
    )
    return jsonify(participant), 201


@api.get("/rounds/code/<code>")
@authenticated
def get_round(code: str):
    return jsonify(_store().get_round(g.golfer["id"], code))


@api.patch("/rounds/<round_id>/current-hole")
@authenticated
def set_current_hole(round_id: str):
    return jsonify(_store().set_current_hole(g.golfer["id"], round_id, _body().get("hole")))


@api.patch("/rounds/<round_id>/status")
@authenticated
def set_status(round_id: str):
    return jsonify(_store().set_status(g.golfer["id"], round_id, _body().get("status")))


@api.put("/rounds/<round_id>/holes/<int:hole>/par")
@authenticated
def set_par(round_id: str, hole: int):
    return jsonify(_store().set_par(g.golfer["id"], round_id, hole, _body().get("par")))


@api.put("/rounds/<round_id>/holes/<int:hole>/score")
@authenticated
def set_score(round_id: str, hole: int):
    payload = _body()
    return jsonify(
        _store().set_score(
            g.golfer["id"],
            round_id,
            hole,
            payload.get("strokes"),
            player_participant_id=payload.get("player_participant_id"),
        )
    )


@api.put("/rounds/<round_id>/holes/<int:hole>/contributions/<shot_type>")
@authenticated
def set_contribution(round_id: str, hole: int, shot_type: str):
    return jsonify(
        _store().set_scramble_contribution(
            g.golfer["id"],
            round_id,
            hole,
            shot_type,
            _body().get("player_participant_id"),
        )
    )


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
