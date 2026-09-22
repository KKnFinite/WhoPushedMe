from __future__ import annotations

import os
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator
from uuid import UUID

import psycopg
from psycopg import errors
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from who_pushed_me.auth import (
    SESSION_TTL,
    generate_recovery_key as generate_account_recovery_key,
    generate_session_token,
    hash_password,
    hash_recovery_key,
    hash_session_token,
    normalize_username,
    verify_password,
)
from who_pushed_me.courses import CourseSnapshot
from who_pushed_me.content.catalog import ContentCatalog, ContentError
from who_pushed_me.content.derived import (
    score_transition_events,
    standing_transition_events,
)
from who_pushed_me.content.preferences import merge_preference_patch, public_preferences
from who_pushed_me.content.presentation import (
    build_shared_presentation,
    filter_presentation_for_preferences,
    par_content_event,
    score_content_event,
    scramble_contribution_content_event,
    score_response_content_event,
    social_content_event,
    status_content_event,
)
from who_pushed_me.routes import build_route
from who_pushed_me.domain import (
    DomainError,
    NotFound,
    PermissionDenied,
    PARTICIPANT_ROLES,
    ROUND_MODES,
    ROUND_STATUSES,
    audit_event_type,
    clean_display_name,
    generate_recovery_key,
    generate_round_code,
    normalize_recovery_key,
    normalize_shot_type,
    require_active_round,
    require_player,
    validate_hole,
    validate_shared_hole_change,
    validate_social_event,
)


class RoundStore:
    def __init__(self, database_url: str | None = None) -> None:
        self.database_url = (
            database_url
            or os.getenv("DATABASE_URL", "")
            or os.getenv("DATABASE_URL_UNPOOLED", "")
        )

    @contextmanager
    def _connection(self) -> Iterator[psycopg.Connection[dict[str, Any]]]:
        if not self.database_url:
            raise RuntimeError("DATABASE_URL is not configured")
        with psycopg.connect(self.database_url, row_factory=dict_row) as connection:
            yield connection

    @staticmethod
    def _uuid(value: object, field: str) -> UUID:
        try:
            return UUID(str(value))
        except (TypeError, ValueError) as error:
            raise DomainError(f"{field} must be a UUID") from error

    @staticmethod
    def _clean_tee_name(value: object | None) -> str | None:
        if value is None:
            return None
        tee_name = str(value).strip()
        if not tee_name:
            return None
        if len(tee_name) > 40:
            raise DomainError("tee_name must be 40 characters or fewer")
        return tee_name

    @staticmethod
    def _validate_course_tee(
        cursor: Any,
        course_id: UUID,
        tee_name: str,
    ) -> None:
        cursor.execute(
            """
            SELECT 1
            FROM cached_course_hole_tees
            WHERE course_id = %s AND lower(tee_name) = lower(%s)
            LIMIT 1
            """,
            (course_id, tee_name),
        )
        if not cursor.fetchone():
            raise DomainError("tee is not available for this course")

    @staticmethod
    def _participant(cursor: Any, round_id: UUID, golfer_id: UUID) -> dict[str, Any]:
        cursor.execute(
            """
            SELECT id, round_id, golfer_id, role, tee_name,
                   participation_state, tracked_from_position
            FROM round_participants
            WHERE round_id = %s AND golfer_id = %s
            """,
            (round_id, golfer_id),
        )
        participant = cursor.fetchone()
        if not participant:
            raise NotFound("golfer is not a participant in this round")
        return participant

    @staticmethod
    def _require_active_player(participant: dict[str, Any], operation: str) -> None:
        require_player(participant["role"], operation)
        if participant.get("participation_state") != "active":
            raise PermissionDenied(f"withdrawn players cannot {operation}")

    @staticmethod
    def _round(cursor: Any, round_id: UUID, *, lock: bool = False) -> dict[str, Any]:
        cursor.execute(
            f"""
            SELECT id, mode, hole_count, active_code, current_hole,
                   current_route_position, par_tracking_enabled, end_reason,
                   status, course_id, free_play_name, scramble_tee_name,
                   created_at, updated_at
            FROM rounds WHERE id = %s{' FOR UPDATE' if lock else ''}
            """,
            (round_id,),
        )
        round_row = cursor.fetchone()
        if not round_row:
            raise NotFound("round not found")
        return round_row

    @staticmethod
    def _route_position(
        cursor: Any,
        round_id: UUID,
        route_position: object,
        *,
        lock: bool = False,
    ) -> dict[str, Any]:
        try:
            position = int(route_position)
        except (TypeError, ValueError) as error:
            raise DomainError("route_position must be a number") from error
        if position < 1:
            raise DomainError("route_position must be at least 1")

        cursor.execute(
            f"""
            SELECT round_id, route_position, hole_number, state, skip_reason
            FROM round_route_positions
            WHERE round_id = %s AND route_position = %s
            {'FOR UPDATE' if lock else ''}
            """,
            (round_id, position),
        )
        row = cursor.fetchone()
        if not row:
            raise DomainError("route_position is not part of this round")
        return row

    @staticmethod
    def _runtime_controls_from_cursor(
        cursor: Any,
        catalog: ContentCatalog,
    ) -> dict[str, Any]:
        cursor.execute(
            """
            SELECT mini_mascots_enabled, trash_talk_enabled
            FROM content_system_settings
            WHERE singleton = true
            """
        )
        settings = cursor.fetchone() or {
            "mini_mascots_enabled": True,
            "trash_talk_enabled": True,
        }

        cursor.execute(
            """
            SELECT event_key, enabled
            FROM content_event_overrides
            ORDER BY event_key
            """
        )
        overrides: dict[str, bool] = {}
        for row in cursor.fetchall():
            try:
                key = catalog.registry.canonical_key(str(row["event_key"]))
            except ContentError:
                continue
            overrides[key] = bool(row["enabled"])

        return {
            "mini_mascots_enabled": bool(settings["mini_mascots_enabled"]),
            "trash_talk_enabled": bool(settings["trash_talk_enabled"]),
            "event_overrides": overrides,
        }

    @staticmethod
    def _preferences_from_cursor(
        cursor: Any,
        golfer_id: UUID,
        catalog: ContentCatalog,
    ) -> dict[str, Any]:
        cursor.execute(
            """
            SELECT mini_mascots_enabled, trash_talk_enabled,
                   max_vulgarity, theme_preferences
            FROM golfer_content_preferences
            WHERE golfer_id = %s
            """,
            (golfer_id,),
        )
        return public_preferences(cursor.fetchone(), catalog.theme_rows)

    def _event(
        self,
        cursor: Any,
        *,
        round_id: UUID,
        actor_participant_id: UUID,
        event_type: str,
        hole_number: int | None = None,
        route_position: int | None = None,
        old_value: object | None = None,
        new_value: object | None = None,
        data: dict[str, object] | None = None,
        reply_to_event_id: UUID | None = None,
        content_event_key: str | None = None,
        presentation_context: dict[str, object] | None = None,
    ) -> dict[str, Any]:
        presentation: dict[str, Any] = {}
        canonical_content_event: str | None = None

        if content_event_key:
            catalog = ContentCatalog.load()
            canonical_content_event = catalog.registry.canonical_key(content_event_key)
            controls = self._runtime_controls_from_cursor(cursor, catalog)
            presentation = build_shared_presentation(
                catalog,
                canonical_content_event,
                controls=controls,
                context=presentation_context,
            )

        event_data = dict(data or {})
        if actor_participant_id:
            cursor.execute(
                """
                SELECT g.id AS golfer_id, g.display_name
                FROM round_participants rp
                JOIN golfers g ON g.id = rp.golfer_id
                WHERE rp.id = %s AND rp.round_id = %s
                """,
                (actor_participant_id, round_id),
            )
            actor_identity = cursor.fetchone()
            if actor_identity:
                event_data.setdefault(
                    "actor_golfer_id",
                    str(actor_identity["golfer_id"]),
                )
                event_data.setdefault(
                    "actor_display_name",
                    actor_identity["display_name"],
                )

        cursor.execute(
            """
            INSERT INTO round_events (
                round_id, actor_participant_id, event_type, hole_number,
                route_position, old_value, new_value, data, reply_to_event_id,
                content_event_key, presentation
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, event_type, hole_number, route_position,
                      old_value, new_value, data, reply_to_event_id,
                      content_event_key, presentation, created_at
            """,
            (
                round_id,
                actor_participant_id,
                event_type,
                hole_number,
                route_position,
                Jsonb(old_value) if old_value is not None else None,
                Jsonb(new_value) if new_value is not None else None,
                Jsonb(event_data),
                reply_to_event_id,
                canonical_content_event,
                Jsonb(presentation),
            ),
        )
        return cursor.fetchone()

    @staticmethod
    def _public_account(row: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": row["id"],
            "username": row.get("username"),
            "display_name": row["display_name"],
            "is_admin": bool(row.get("is_admin", False)),
            "created_at": row["created_at"],
        }

    @staticmethod
    def _issue_session(cursor: Any, golfer_id: UUID) -> dict[str, Any]:
        token = generate_session_token()
        token_hash = hash_session_token(token)
        expires_at = datetime.now(timezone.utc) + SESSION_TTL
        cursor.execute(
            """
            INSERT INTO auth_sessions (golfer_id, token_hash, expires_at)
            VALUES (%s, %s, %s)
            RETURNING id, created_at, expires_at
            """,
            (golfer_id, token_hash, expires_at),
        )
        session = cursor.fetchone()
        return {
            "token": token,
            "session_id": session["id"],
            "created_at": session["created_at"],
            "expires_at": session["expires_at"],
        }

    def register_account(
        self,
        *,
        username: object,
        password: object,
        display_name: object,
    ) -> dict[str, Any]:
        normalized_username = normalize_username(username)
        name = clean_display_name(display_name)
        password_hash = hash_password(password)

        for _ in range(8):
            recovery_key = generate_account_recovery_key()
            recovery_hash = hash_recovery_key(recovery_key)
            try:
                with self._connection() as connection, connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO golfers (
                            display_name,
                            username,
                            password_hash,
                            recovery_key_hash,
                            recovery_key
                        )
                        VALUES (%s, %s, %s, %s, NULL)
                        RETURNING id, username, display_name, is_admin, created_at
                        """,
                        (
                            name,
                            normalized_username,
                            password_hash,
                            recovery_hash,
                        ),
                    )
                    golfer = cursor.fetchone()
                    session = self._issue_session(cursor, golfer["id"])
                    return {
                        "account": self._public_account(golfer),
                        "session": session,
                        "recovery_key": recovery_key,
                    }
            except errors.UniqueViolation as error:
                constraint = error.diag.constraint_name or ""
                if constraint == "golfers_username_lower_unique":
                    raise DomainError("username is already taken") from error
                if constraint == "golfers_recovery_key_hash_unique":
                    continue
                raise

        raise RuntimeError("could not allocate a unique recovery key")

    def recover_account_with_key(
        self,
        *,
        recovery_key: object,
        new_password: object,
    ) -> dict[str, Any]:
        recovery_hash = hash_recovery_key(recovery_key)
        password_hash = hash_password(new_password)

        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, username, display_name, is_admin, created_at
                FROM golfers
                WHERE recovery_key_hash = %s
                FOR UPDATE
                """,
                (recovery_hash,),
            )
            golfer = cursor.fetchone()
            if not golfer:
                raise PermissionDenied("invalid recovery key")

            replacement_key = generate_account_recovery_key()
            replacement_hash = hash_recovery_key(replacement_key)

            cursor.execute(
                """
                UPDATE golfers
                SET password_hash = %s,
                    recovery_key_hash = %s,
                    recovery_key = NULL
                WHERE id = %s
                """,
                (password_hash, replacement_hash, golfer["id"]),
            )
            cursor.execute(
                """
                UPDATE auth_sessions
                SET revoked_at = now()
                WHERE golfer_id = %s
                  AND revoked_at IS NULL
                """,
                (golfer["id"],),
            )

            session = self._issue_session(cursor, golfer["id"])
            return {
                "account": self._public_account(golfer),
                "session": session,
                "recovery_key": replacement_key,
                "recovery_key_rotated": True,
            }

    def login_account(
        self,
        *,
        username: object,
        password: object,
    ) -> dict[str, Any]:
        normalized_username = normalize_username(username)
        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, username, display_name, password_hash,
                       is_admin, created_at
                FROM golfers
                WHERE lower(username) = %s
                """,
                (normalized_username,),
            )
            golfer = cursor.fetchone()
            if (
                not golfer
                or not golfer.get("password_hash")
                or not verify_password(golfer["password_hash"], password)
            ):
                raise PermissionDenied("invalid username or password")

            session = self._issue_session(cursor, golfer["id"])
            return {
                "account": self._public_account(golfer),
                "session": session,
            }

    def logout_session(self, token: object) -> dict[str, bool]:
        token_hash = hash_session_token(token)
        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE auth_sessions
                SET revoked_at = now()
                WHERE token_hash = %s
                  AND revoked_at IS NULL
                RETURNING id
                """,
                (token_hash,),
            )
            if not cursor.fetchone():
                raise PermissionDenied("invalid or expired session")
            return {"logged_out": True}

    def authenticate_session(self, token: object) -> dict[str, Any]:
        token_hash = hash_session_token(token)
        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT g.id, g.username, g.display_name, g.is_admin, g.created_at,
                       s.id AS session_id, s.expires_at
                FROM auth_sessions s
                JOIN golfers g ON g.id = s.golfer_id
                WHERE s.token_hash = %s
                  AND s.revoked_at IS NULL
                  AND s.expires_at > now()
                """,
                (token_hash,),
            )
            golfer = cursor.fetchone()
            if not golfer:
                raise PermissionDenied("invalid or expired session")

            cursor.execute(
                """
                UPDATE auth_sessions
                SET last_seen_at = now()
                WHERE id = %s
                """,
                (golfer["session_id"],),
            )
            account = self._public_account(golfer)
            account["session_id"] = golfer["session_id"]
            account["session_expires_at"] = golfer["expires_at"]
            return account

    def create_golfer(self, display_name: object) -> dict[str, Any]:
        name = clean_display_name(display_name)
        for _ in range(8):
            key = generate_recovery_key()
            try:
                with self._connection() as connection, connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO golfers (display_name, recovery_key)
                        VALUES (%s, %s)
                        RETURNING id, display_name, recovery_key, created_at
                        """,
                        (name, key),
                    )
                    return cursor.fetchone()
            except errors.UniqueViolation:
                continue
        raise RuntimeError("could not allocate a unique recovery key")

    def recover_golfer(self, recovery_key: object) -> dict[str, Any]:
        key = normalize_recovery_key(recovery_key)
        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, display_name, recovery_key, created_at FROM golfers WHERE recovery_key = %s",
                (key,),
            )
            golfer = cursor.fetchone()
            if not golfer:
                raise NotFound("recovery key not found")
            return golfer

    def get_content_preferences(self, golfer_id: object) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        catalog = ContentCatalog.load()
        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT mini_mascots_enabled, trash_talk_enabled,
                       max_vulgarity, theme_preferences
                FROM golfer_content_preferences
                WHERE golfer_id = %s
                """,
                (golfer_uuid,),
            )
            return public_preferences(cursor.fetchone(), catalog.theme_rows)

    def update_content_preferences(
        self,
        golfer_id: object,
        patch: dict[str, Any],
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        if not isinstance(patch, dict):
            raise DomainError("preferences patch must be a JSON object")

        catalog = ContentCatalog.load()
        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT mini_mascots_enabled, trash_talk_enabled,
                       max_vulgarity, theme_preferences
                FROM golfer_content_preferences
                WHERE golfer_id = %s
                FOR UPDATE
                """,
                (golfer_uuid,),
            )
            current = cursor.fetchone()
            try:
                merged = merge_preference_patch(current, patch, catalog.theme_rows)
            except ContentError as error:
                raise DomainError(str(error)) from error

            cursor.execute(
                """
                INSERT INTO golfer_content_preferences (
                    golfer_id,
                    mini_mascots_enabled,
                    trash_talk_enabled,
                    max_vulgarity,
                    theme_preferences,
                    updated_at
                )
                VALUES (%s, %s, %s, %s, %s, now())
                ON CONFLICT (golfer_id)
                DO UPDATE SET
                    mini_mascots_enabled = EXCLUDED.mini_mascots_enabled,
                    trash_talk_enabled = EXCLUDED.trash_talk_enabled,
                    max_vulgarity = EXCLUDED.max_vulgarity,
                    theme_preferences = EXCLUDED.theme_preferences,
                    updated_at = now()
                RETURNING mini_mascots_enabled, trash_talk_enabled,
                          max_vulgarity, theme_preferences
                """,
                (
                    golfer_uuid,
                    merged["mini_mascots_enabled"],
                    merged["trash_talk_enabled"],
                    merged["max_vulgarity"],
                    Jsonb(merged["theme_preferences"]),
                ),
            )
            return public_preferences(cursor.fetchone(), catalog.theme_rows)

    def get_content_runtime_controls(self) -> dict[str, Any]:
        catalog = ContentCatalog.load()
        with self._connection() as connection, connection.cursor() as cursor:
            return self._runtime_controls_from_cursor(cursor, catalog)

    def set_content_runtime_master(
        self,
        *,
        mini_mascots_enabled: bool | None = None,
        trash_talk_enabled: bool | None = None,
    ) -> dict[str, Any]:
        if mini_mascots_enabled is not None and not isinstance(
            mini_mascots_enabled, bool
        ):
            raise DomainError("mini_mascots_enabled must be true or false")
        if trash_talk_enabled is not None and not isinstance(
            trash_talk_enabled, bool
        ):
            raise DomainError("trash_talk_enabled must be true or false")

        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO content_system_settings (singleton)
                VALUES (true)
                ON CONFLICT (singleton) DO NOTHING
                """
            )
            if mini_mascots_enabled is not None:
                cursor.execute(
                    """
                    UPDATE content_system_settings
                    SET mini_mascots_enabled = %s, updated_at = now()
                    WHERE singleton = true
                    """,
                    (mini_mascots_enabled,),
                )
            if trash_talk_enabled is not None:
                cursor.execute(
                    """
                    UPDATE content_system_settings
                    SET trash_talk_enabled = %s, updated_at = now()
                    WHERE singleton = true
                    """,
                    (trash_talk_enabled,),
                )
        return self.get_content_runtime_controls()

    def set_content_event_override(
        self,
        event_key: object,
        enabled: bool | None,
    ) -> dict[str, Any]:
        catalog = ContentCatalog.load()
        key = catalog.registry.canonical_key(str(event_key or ""))

        if enabled is not None and not isinstance(enabled, bool):
            raise DomainError("event override must be true, false, or default")

        with self._connection() as connection, connection.cursor() as cursor:
            if enabled is None:
                cursor.execute(
                    "DELETE FROM content_event_overrides WHERE event_key = %s",
                    (key,),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO content_event_overrides (event_key, enabled, updated_at)
                    VALUES (%s, %s, now())
                    ON CONFLICT (event_key)
                    DO UPDATE SET enabled = EXCLUDED.enabled, updated_at = now()
                    """,
                    (key, enabled),
                )
        return self.get_content_runtime_controls()

    def create_round(
        self,
        golfer_id: object,
        *,
        mode: object,
        holes: object,
        course_id: object | None = None,
        free_play_name: object | None = None,
        tee_name: object | None = None,
        start_hole: object = 1,
        end_hole: object | None = None,
        course_hole_count: object | None = None,
        par_tracking_enabled: object = True,
        tracking_start_position: object = 1,
        prior_holes_mode: object = "untracked",
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_mode = str(mode or "")
        if round_mode not in ROUND_MODES:
            raise DomainError("mode must be individual or scramble")

        try:
            requested_holes = int(holes)
        except (TypeError, ValueError) as error:
            raise DomainError("holes must be a positive number") from error
        if not 1 <= requested_holes <= 99:
            raise DomainError("holes must be between 1 and 99")

        if not isinstance(par_tracking_enabled, bool):
            raise DomainError("par_tracking_enabled must be true or false")

        try:
            requested_tracking_start = int(tracking_start_position)
        except (TypeError, ValueError) as error:
            raise DomainError(
                "tracking_start_position must be a number"
            ) from error
        prior_mode = str(prior_holes_mode or "untracked").strip().lower()
        if prior_mode not in {"untracked", "backfill"}:
            raise DomainError(
                "prior_holes_mode must be untracked or backfill"
            )

        cached_course_id = self._uuid(course_id, "course_id") if course_id else None
        free_play = str(free_play_name).strip() if free_play_name else None
        creator_tee = self._clean_tee_name(tee_name)
        scramble_tee = creator_tee if round_mode == "scramble" else None
        participant_tee = creator_tee if round_mode == "individual" else None

        if cached_course_id and free_play:
            raise DomainError("choose a cached course or Free Play, not both")
        if not cached_course_id and not free_play:
            raise DomainError("choose a course or enter a Free Play name")

        for _ in range(12):
            try:
                with self._connection() as connection, connection.cursor() as cursor:
                    physical_hole_count: int

                    if cached_course_id:
                        cursor.execute(
                            """
                            SELECT max(hole_number) AS max_hole
                            FROM cached_course_holes
                            WHERE course_id = %s
                            """,
                            (cached_course_id,),
                        )
                        course_row = cursor.fetchone()
                        max_hole = int(course_row["max_hole"] or 0)
                        if max_hole < 1:
                            raise NotFound("cached course has no hole data")
                        physical_hole_count = 9 if max_hole <= 9 else 18

                        if creator_tee:
                            self._validate_course_tee(
                                cursor,
                                cached_course_id,
                                creator_tee,
                            )
                    else:
                        if course_hole_count is None:
                            physical_hole_count = (
                                9 if requested_holes <= 9 else 18
                            )
                        else:
                            try:
                                physical_hole_count = int(course_hole_count)
                            except (TypeError, ValueError) as error:
                                raise DomainError(
                                    "course_hole_count must be 9 or 18"
                                ) from error
                            if physical_hole_count not in {9, 18}:
                                raise DomainError(
                                    "course_hole_count must be 9 or 18"
                                )

                    if end_hole is None:
                        route = build_route(
                            course_hole_count=physical_hole_count,
                            start_hole=start_hole,
                            hole_count=requested_holes,
                        )
                    else:
                        route = build_route(
                            course_hole_count=physical_hole_count,
                            start_hole=start_hole,
                            end_hole=end_hole,
                        )

                    route_length = len(route)
                    if not 1 <= requested_tracking_start <= route_length:
                        raise DomainError(
                            "tracking_start_position must be within the round route"
                        )
                    first_hole = route[0].hole_number
                    current_route = route[requested_tracking_start - 1]
                    current_hole = current_route.hole_number
                    participant_tracked_from = (
                        requested_tracking_start
                        if prior_mode == "untracked"
                        else 1
                    )
                    code = generate_round_code()

                    cursor.execute(
                        """
                        INSERT INTO rounds (
                            mode, hole_count, active_code, current_hole,
                            current_route_position, par_tracking_enabled,
                            status, course_id, free_play_name,
                            scramble_tee_name
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, 'setup', %s, %s, %s)
                        RETURNING id, mode, hole_count, active_code,
                                  current_hole, current_route_position,
                                  par_tracking_enabled, status, course_id,
                                  free_play_name, scramble_tee_name, created_at
                        """,
                        (
                            round_mode,
                            route_length,
                            code,
                            current_hole,
                            requested_tracking_start,
                            par_tracking_enabled,
                            cached_course_id,
                            free_play,
                            scramble_tee,
                        ),
                    )
                    round_row = cursor.fetchone()

                    cursor.executemany(
                        """
                        INSERT INTO round_route_positions (
                            round_id, route_position, hole_number,
                            state, skip_reason
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        [
                            (
                                round_row["id"],
                                item.route_position,
                                item.hole_number,
                                (
                                    "skipped"
                                    if (
                                        prior_mode == "untracked"
                                        and item.route_position
                                        < requested_tracking_start
                                    )
                                    else "planned"
                                ),
                                (
                                    "untracked_before_app"
                                    if (
                                        prior_mode == "untracked"
                                        and item.route_position
                                        < requested_tracking_start
                                    )
                                    else None
                                ),
                            )
                            for item in route
                        ],
                    )

                    cursor.execute(
                        """
                        INSERT INTO round_participants (
                            round_id, golfer_id, role, tee_name,
                            participation_state, tracked_from_position
                        )
                        VALUES (%s, %s, 'player', %s, 'active', %s)
                        RETURNING id, tee_name, participation_state,
                                  tracked_from_position
                        """,
                        (
                            round_row["id"],
                            golfer_uuid,
                            participant_tee,
                            participant_tracked_from,
                        ),
                    )
                    participant = cursor.fetchone()

                    cursor.executemany(
                        """
                        INSERT INTO round_participant_route_positions (
                            round_id, participant_id, route_position, required
                        )
                        VALUES (%s, %s, %s, true)
                        """,
                        [
                            (
                                round_row["id"],
                                participant["id"],
                                item.route_position,
                            )
                            for item in route
                            if not (
                                prior_mode == "untracked"
                                and item.route_position
                                < requested_tracking_start
                            )
                        ],
                    )

                    self._event(
                        cursor,
                        round_id=round_row["id"],
                        actor_participant_id=participant["id"],
                        event_type="lobby_created",
                        data={
                            "role": "player",
                            "start_hole": first_hole,
                            "live_hole": current_hole,
                            "route_length": route_length,
                            "tracking_start_position": requested_tracking_start,
                            "prior_holes_mode": prior_mode,
                        },
                        content_event_key="lobby.created",
                        presentation_context={"mode": round_mode},
                    )

                    if cached_course_id and par_tracking_enabled:
                        cursor.execute(
                            """
                            INSERT INTO round_route_pars (
                                round_id, route_position, par, source
                            )
                            SELECT rr.round_id, rr.route_position, ch.par, 'course'
                            FROM round_route_positions rr
                            JOIN cached_course_holes ch
                              ON ch.course_id = %s
                             AND ch.hole_number = rr.hole_number
                            WHERE rr.round_id = %s
                              AND ch.par IS NOT NULL
                            """,
                            (cached_course_id, round_row["id"]),
                        )
                        cursor.execute(
                            """
                            INSERT INTO round_hole_pars (
                                round_id, hole_number, par
                            )
                            SELECT DISTINCT %s, ch.hole_number, ch.par
                            FROM cached_course_holes ch
                            JOIN round_route_positions rr
                              ON rr.round_id = %s
                             AND rr.hole_number = ch.hole_number
                            WHERE ch.course_id = %s
                              AND ch.par IS NOT NULL
                            ON CONFLICT (round_id, hole_number)
                            DO UPDATE SET par = EXCLUDED.par,
                                          updated_at = now()
                            """,
                            (
                                round_row["id"],
                                round_row["id"],
                                cached_course_id,
                            ),
                        )

                    round_row["participant_id"] = participant["id"]
                    round_row["role"] = "player"
                    round_row["tee_name"] = (
                        round_row["scramble_tee_name"]
                        if round_mode == "scramble"
                        else participant["tee_name"]
                    )
                    round_row["route"] = [
                        item.as_dict()
                        for item in route
                    ]
                    return round_row
            except errors.UniqueViolation as error:
                if error.diag.constraint_name != "rounds_live_code_unique":
                    raise

        raise RuntimeError("could not allocate a unique active round code")

    def join_round(
        self,
        golfer_id: object,
        *,
        code: object,
        role: object,
        tee_name: object | None = None,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_code = str(code or "").strip()
        participant_role = str(role or "")
        selected_tee = self._clean_tee_name(tee_name)

        if len(round_code) != 4 or not round_code.isdigit():
            raise DomainError("round code must be four digits")
        if participant_role not in PARTICIPANT_ROLES:
            raise DomainError("role must be player or spectator")

        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, mode, course_id, status,
                       current_route_position, hole_count,
                       scramble_tee_name
                FROM rounds
                WHERE active_code = %s
                  AND status IN ('setup', 'active')
                FOR UPDATE
                """,
                (round_code,),
            )
            round_row = cursor.fetchone()
            if not round_row:
                raise NotFound("active round not found")

            if participant_role == "spectator":
                selected_tee = None
            else:
                cursor.execute(
                    """
                    SELECT count(*) AS active_players
                    FROM round_participants
                    WHERE round_id = %s
                      AND role = 'player'
                      AND participation_state = 'active'
                    """,
                    (round_row["id"],),
                )
                if int(cursor.fetchone()["active_players"]) >= 4:
                    raise DomainError("this round already has 4 active golfers")

                if round_row["mode"] == "scramble":
                    selected_tee = None
                elif selected_tee and round_row["course_id"]:
                    self._validate_course_tee(
                        cursor,
                        round_row["course_id"],
                        selected_tee,
                    )

            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM round_participants
                    WHERE golfer_id = %s
                      AND round_id <> %s
                      AND role = 'player'
                ) AS played_before
                """,
                (golfer_uuid, round_row["id"]),
            )
            played_before = bool(cursor.fetchone()["played_before"])

            tracked_from = (
                1
                if round_row["status"] == "setup"
                else int(round_row["current_route_position"])
            )

            cursor.execute(
                """
                INSERT INTO round_participants (
                    round_id, golfer_id, role, tee_name,
                    participation_state, tracked_from_position
                )
                VALUES (%s, %s, %s, %s, 'active', %s)
                ON CONFLICT (round_id, golfer_id) DO NOTHING
                RETURNING id, round_id, golfer_id, role, tee_name,
                          participation_state, tracked_from_position, joined_at
                """,
                (
                    round_row["id"],
                    golfer_uuid,
                    participant_role,
                    selected_tee,
                    tracked_from,
                ),
            )
            participant = cursor.fetchone()

            if participant:
                if participant_role == "player":
                    cursor.execute(
                        """
                        INSERT INTO round_participant_route_positions (
                            round_id, participant_id, route_position, required
                        )
                        SELECT %s, %s, rr.route_position, true
                        FROM round_route_positions rr
                        WHERE rr.round_id = %s
                          AND rr.route_position >= %s
                          AND rr.state = 'planned'
                        ON CONFLICT (participant_id, route_position)
                        DO NOTHING
                        """,
                        (
                            round_row["id"],
                            participant["id"],
                            round_row["id"],
                            tracked_from,
                        ),
                    )

                if participant_role == "spectator":
                    content_event = "lobby.join.spectator"
                elif played_before:
                    content_event = "lobby.join.returning_player"
                else:
                    content_event = "lobby.join.new_player"

                self._event(
                    cursor,
                    round_id=round_row["id"],
                    actor_participant_id=participant["id"],
                    event_type="participant_join",
                    route_position=(
                        tracked_from
                        if participant_role == "player"
                        else None
                    ),
                    data={
                        "role": participant_role,
                        "tracked_from_position": (
                            tracked_from
                            if participant_role == "player"
                            else None
                        ),
                    },
                    content_event_key=content_event,
                    presentation_context={"mode": round_row["mode"]},
                )
                return participant

            cursor.execute(
                """
                SELECT id, round_id, golfer_id, role, tee_name,
                       participation_state, tracked_from_position, joined_at
                FROM round_participants
                WHERE round_id = %s AND golfer_id = %s
                """,
                (round_row["id"], golfer_uuid),
            )
            participant = cursor.fetchone()
            reconnect_event = (
                "lobby.reconnect.spectator"
                if participant["role"] == "spectator"
                else "lobby.reconnect.player"
            )
            self._event(
                cursor,
                round_id=round_row["id"],
                actor_participant_id=participant["id"],
                event_type="participant_reconnect",
                route_position=round_row["current_route_position"],
                data={"role": participant["role"]},
                content_event_key=reconnect_event,
                presentation_context={"mode": round_row["mode"]},
            )
            return participant

    def set_participation_state(
        self,
        golfer_id: object,
        round_id: object,
        state: object,
        *,
        reason: object | None = None,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        requested = str(state or "").strip().lower()
        if requested not in {"active", "withdrew"}:
            raise DomainError("participation state must be active or withdrew")

        surrender_reason = str(reason or "").strip()
        if len(surrender_reason) > 280:
            raise DomainError("surrender reason must be 280 characters or fewer")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            participant = self._participant(cursor, round_uuid, golfer_uuid)
            require_player(participant["role"], "change participation state")
            require_active_round(round_row["status"], "change participation state")

            old_state = str(participant.get("participation_state") or "active")
            if old_state == requested:
                return {
                    "round_id": round_uuid,
                    "participant_id": participant["id"],
                    "participation_state": requested,
                    "event": None,
                }

            current_position = int(round_row["current_route_position"])
            if requested == "active":
                cursor.execute(
                    """
                    SELECT count(*) AS active_players
                    FROM round_participants
                    WHERE round_id = %s
                      AND role = 'player'
                      AND participation_state = 'active'
                      AND id <> %s
                    """,
                    (round_uuid, participant["id"]),
                )
                if int(cursor.fetchone()["active_players"] or 0) >= 4:
                    raise DomainError("this round already has 4 active golfers")

            cursor.execute(
                """
                UPDATE round_participants
                SET participation_state = %s
                WHERE id = %s
                """,
                (requested, participant["id"]),
            )

            if round_row["mode"] == "individual":
                if requested == "withdrew":
                    cursor.execute(
                        """
                        UPDATE round_participant_route_positions
                        SET required = false
                        WHERE participant_id = %s
                          AND route_position >= %s
                        """,
                        (participant["id"], current_position),
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO round_participant_route_positions (
                            round_id, participant_id, route_position, required
                        )
                        SELECT %s, %s, route_position, true
                        FROM round_route_positions
                        WHERE round_id = %s
                          AND route_position >= %s
                          AND state = 'planned'
                        ON CONFLICT (participant_id, route_position)
                        DO UPDATE SET required = true
                        """,
                        (
                            round_uuid,
                            participant["id"],
                            round_uuid,
                            current_position,
                        ),
                    )

            route_row = self._route_position(
                cursor,
                round_uuid,
                current_position,
            )
            event = self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=participant["id"],
                event_type=(
                    "participant_withdrew"
                    if requested == "withdrew"
                    else "participant_returned"
                ),
                hole_number=int(route_row["hole_number"]),
                route_position=current_position,
                data={
                    "participant_id": str(participant["id"]),
                    "reason": surrender_reason or None,
                    "mode": round_row["mode"],
                },
                content_event_key=(
                    "participant.towel"
                    if requested == "withdrew"
                    else "participant.return"
                ),
                presentation_context={
                    "mode": round_row["mode"],
                    "reason": surrender_reason,
                },
            )
            return {
                "round_id": round_uuid,
                "participant_id": participant["id"],
                "participation_state": requested,
                "event": event,
            }

    def promote_spectator_to_player(
        self,
        golfer_id: object,
        round_id: object,
        *,
        tee_name: object | None = None,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        selected_tee = self._clean_tee_name(tee_name)

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            participant = self._participant(cursor, round_uuid, golfer_uuid)

            if round_row["status"] != "active":
                raise DomainError(
                    "spectators can only join play during an active round"
                )
            if participant["role"] == "player":
                return participant
            if participant["role"] != "spectator":
                raise DomainError("only spectators can join play this way")

            cursor.execute(
                """
                SELECT count(*) AS active_players
                FROM round_participants
                WHERE round_id = %s
                  AND role = 'player'
                  AND participation_state = 'active'
                """,
                (round_uuid,),
            )
            if int(cursor.fetchone()["active_players"] or 0) >= 4:
                raise DomainError("this round already has 4 active golfers")

            if round_row["mode"] == "scramble":
                selected_tee = None
            elif round_row["course_id"]:
                cursor.execute(
                    """
                    SELECT EXISTS (
                        SELECT 1
                        FROM cached_course_hole_tees
                        WHERE course_id = %s
                    ) AS has_tees
                    """,
                    (round_row["course_id"],),
                )
                has_tees = bool(cursor.fetchone()["has_tees"])
                if has_tees and not selected_tee:
                    raise DomainError("choose a tee before joining as a player")
                if selected_tee:
                    self._validate_course_tee(
                        cursor,
                        round_row["course_id"],
                        selected_tee,
                    )

            tracked_from = int(round_row["current_route_position"])
            cursor.execute(
                """
                UPDATE round_participants
                SET role = 'player',
                    tee_name = %s,
                    participation_state = 'active',
                    tracked_from_position = %s
                WHERE id = %s
                RETURNING id, round_id, golfer_id, role, tee_name,
                          participation_state, tracked_from_position, joined_at
                """,
                (selected_tee, tracked_from, participant["id"]),
            )
            promoted = cursor.fetchone()

            cursor.execute(
                """
                INSERT INTO round_participant_route_positions (
                    round_id, participant_id, route_position, required
                )
                SELECT %s, %s, rr.route_position, true
                FROM round_route_positions rr
                WHERE rr.round_id = %s
                  AND rr.route_position >= %s
                  AND rr.state = 'planned'
                ON CONFLICT (participant_id, route_position)
                DO UPDATE SET required = true
                """,
                (
                    round_uuid,
                    participant["id"],
                    round_uuid,
                    tracked_from,
                ),
            )

            route_row = self._route_position(
                cursor,
                round_uuid,
                tracked_from,
            )
            self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=participant["id"],
                event_type="spectator_joined_play",
                hole_number=int(route_row["hole_number"]),
                route_position=tracked_from,
                data={
                    "participant_id": str(participant["id"]),
                    "tracked_from_position": tracked_from,
                    "tee_name": selected_tee,
                },
                content_event_key="participant.spectator_to_player",
                presentation_context={
                    "mode": round_row["mode"],
                    "hole": int(route_row["hole_number"]),
                },
            )
            return promoted

    def add_round_only_player(
        self,
        golfer_id: object,
        round_id: object,
        *,
        display_name: object,
        tee_name: object | None = None,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        name = clean_display_name(display_name)
        selected_tee = self._clean_tee_name(tee_name)

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            actor = self._participant(cursor, round_uuid, golfer_uuid)
            self._require_active_player(actor, "add an offline golfer")

            if round_row["status"] not in {"setup", "active"}:
                raise DomainError(
                    "offline golfers can only be added before or during an active round"
                )

            cursor.execute(
                """
                SELECT count(*) AS active_players
                FROM round_participants
                WHERE round_id = %s
                  AND role = 'player'
                  AND participation_state = 'active'
                """,
                (round_uuid,),
            )
            if int(cursor.fetchone()["active_players"] or 0) >= 4:
                raise DomainError("this round already has 4 active golfers")

            if round_row["mode"] == "scramble":
                selected_tee = None
            elif round_row["course_id"]:
                cursor.execute(
                    """
                    SELECT EXISTS (
                        SELECT 1
                        FROM cached_course_hole_tees
                        WHERE course_id = %s
                    ) AS has_tees
                    """,
                    (round_row["course_id"],),
                )
                has_tees = bool(cursor.fetchone()["has_tees"])
                if has_tees and not selected_tee:
                    raise DomainError(
                        "choose a tee for the offline golfer"
                    )
                if selected_tee:
                    self._validate_course_tee(
                        cursor,
                        round_row["course_id"],
                        selected_tee,
                    )

            tracked_from = (
                1
                if round_row["status"] == "setup"
                else int(round_row["current_route_position"])
            )

            cursor.execute(
                """
                INSERT INTO golfers (display_name)
                VALUES (%s)
                RETURNING id, display_name
                """,
                (name,),
            )
            round_only_golfer = cursor.fetchone()

            cursor.execute(
                """
                INSERT INTO round_participants (
                    round_id, golfer_id, role, tee_name,
                    participation_state, tracked_from_position
                )
                VALUES (%s, %s, 'player', %s, 'active', %s)
                RETURNING id, round_id, golfer_id, role, tee_name,
                          participation_state, tracked_from_position, joined_at
                """,
                (
                    round_uuid,
                    round_only_golfer["id"],
                    selected_tee,
                    tracked_from,
                ),
            )
            participant = cursor.fetchone()

            cursor.execute(
                """
                INSERT INTO round_participant_route_positions (
                    round_id, participant_id, route_position, required
                )
                SELECT %s, %s, rr.route_position, true
                FROM round_route_positions rr
                WHERE rr.round_id = %s
                  AND rr.route_position >= %s
                  AND rr.state = 'planned'
                ON CONFLICT (participant_id, route_position)
                DO UPDATE SET required = true
                """,
                (
                    round_uuid,
                    participant["id"],
                    round_uuid,
                    tracked_from,
                ),
            )

            route_position = (
                tracked_from
                if round_row["status"] == "active"
                else None
            )
            hole_number = None
            if route_position is not None:
                hole_number = int(
                    self._route_position(
                        cursor,
                        round_uuid,
                        route_position,
                    )["hole_number"]
                )

            self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=actor["id"],
                event_type="participant_proxy_added",
                hole_number=hole_number,
                route_position=route_position,
                data={
                    "player_participant_id": str(participant["id"]),
                    "display_name": name,
                    "round_only": True,
                    "tracked_from_position": tracked_from,
                },
                content_event_key="participant.proxy_added",
                presentation_context={
                    "mode": round_row["mode"],
                    "subject": name,
                    "hole": hole_number or "",
                },
            )

            participant["display_name"] = name
            participant["round_only"] = True
            return participant

    def list_claimable_round_only_players(
        self,
        golfer_id: object,
        code: object,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_code = str(code or "").strip()
        if len(round_code) != 4 or not round_code.isdigit():
            raise DomainError("round code must be four digits")

        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, active_code, status, mode
                FROM rounds
                WHERE active_code = %s
                  AND status IN ('setup', 'active')
                """,
                (round_code,),
            )
            round_row = cursor.fetchone()
            if not round_row:
                raise NotFound("active round not found")

            cursor.execute(
                """
                SELECT 1
                FROM round_participants
                WHERE round_id = %s AND golfer_id = %s
                LIMIT 1
                """,
                (round_row["id"], golfer_uuid),
            )
            if cursor.fetchone():
                return {
                    "round_id": round_row["id"],
                    "active_code": round_code,
                    "players": [],
                }

            cursor.execute(
                """
                SELECT rp.id AS participant_id, g.display_name,
                       rp.tee_name, rp.participation_state,
                       rp.tracked_from_position
                FROM round_participants rp
                JOIN golfers g ON g.id = rp.golfer_id
                WHERE rp.round_id = %s
                  AND rp.role = 'player'
                  AND rp.participation_state <> 'removed'
                  AND g.username IS NULL
                  AND g.password_hash IS NULL
                  AND g.recovery_key_hash IS NULL
                  AND g.recovery_key IS NULL
                ORDER BY rp.joined_at, rp.id
                """,
                (round_row["id"],),
            )
            return {
                "round_id": round_row["id"],
                "active_code": round_code,
                "players": cursor.fetchall(),
            }

    def claim_round_only_player(
        self,
        golfer_id: object,
        round_id: object,
        participant_id: object,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        participant_uuid = self._uuid(participant_id, "participant_id")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            if round_row["status"] not in {"setup", "active"}:
                raise DomainError(
                    "round-only golfers can only be claimed before the round ends"
                )

            cursor.execute(
                """
                SELECT 1
                FROM round_participants
                WHERE round_id = %s AND golfer_id = %s
                LIMIT 1
                """,
                (round_uuid, golfer_uuid),
            )
            if cursor.fetchone():
                raise DomainError(
                    "this account is already a participant in the round"
                )

            cursor.execute(
                """
                SELECT rp.id, rp.golfer_id, rp.role, rp.tee_name,
                       rp.participation_state, rp.tracked_from_position,
                       g.display_name
                FROM round_participants rp
                JOIN golfers g ON g.id = rp.golfer_id
                WHERE rp.id = %s
                  AND rp.round_id = %s
                  AND rp.role = 'player'
                  AND g.username IS NULL
                  AND g.password_hash IS NULL
                  AND g.recovery_key_hash IS NULL
                  AND g.recovery_key IS NULL
                FOR UPDATE
                """,
                (participant_uuid, round_uuid),
            )
            target = cursor.fetchone()
            if not target:
                raise DomainError(
                    "that player is not an unclaimed round-only golfer"
                )

            old_golfer_id = target["golfer_id"]
            old_display_name = target["display_name"]

            cursor.execute(
                """
                UPDATE round_participants
                SET golfer_id = %s
                WHERE id = %s
                RETURNING id, round_id, golfer_id, role, tee_name,
                          participation_state, tracked_from_position, joined_at
                """,
                (golfer_uuid, participant_uuid),
            )
            claimed = cursor.fetchone()

            cursor.execute(
                "SELECT display_name FROM golfers WHERE id = %s",
                (golfer_uuid,),
            )
            account = cursor.fetchone()

            self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=participant_uuid,
                event_type="participant_claimed",
                data={
                    "player_participant_id": str(participant_uuid),
                    "round_only_golfer_id": str(old_golfer_id),
                    "old_display_name": old_display_name,
                    "display_name": account["display_name"],
                },
                content_event_key="participant.claimed",
                presentation_context={
                    "mode": round_row["mode"],
                    "subject": account["display_name"],
                },
            )

            claimed["display_name"] = account["display_name"]
            claimed["round_only"] = False
            return claimed

    @staticmethod
    def _claim_undo_state_from_cursor(
        cursor: Any,
        round_id: UUID,
        participant_id: UUID,
    ) -> dict[str, Any] | None:
        cursor.execute(
            """
            SELECT id, data, created_at
            FROM round_events
            WHERE round_id = %s
              AND actor_participant_id = %s
              AND event_type = 'participant_claimed'
            ORDER BY created_at DESC, id DESC
            LIMIT 1
            """,
            (round_id, participant_id),
        )
        claim_event = cursor.fetchone()
        if not claim_event:
            return None

        claim_data = claim_event.get("data") or {}
        round_only_golfer_id = claim_data.get("round_only_golfer_id")
        if not round_only_golfer_id:
            return None

        cursor.execute(
            """
            SELECT count(*) AS actions
            FROM round_events
            WHERE round_id = %s
              AND actor_participant_id = %s
              AND created_at > %s
              AND id <> %s
            """,
            (
                round_id,
                participant_id,
                claim_event["created_at"],
                claim_event["id"],
            ),
        )
        actions = int(cursor.fetchone()["actions"] or 0)
        return {
            "available": True,
            "claim_event_id": claim_event["id"],
            "round_only_golfer_id": round_only_golfer_id,
            "old_display_name": claim_data.get("old_display_name"),
            "actions_after_claim": actions,
            "requires_confirmation": actions > 0,
        }

    def undo_round_only_claim(
        self,
        golfer_id: object,
        round_id: object,
        *,
        confirm_actor_history: bool = False,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            if round_row["status"] != "active":
                raise DomainError(
                    "a player claim can only be undone during an active round"
                )

            participant = self._participant(
                cursor,
                round_uuid,
                golfer_uuid,
            )
            state = self._claim_undo_state_from_cursor(
                cursor,
                round_uuid,
                participant["id"],
            )
            if not state:
                raise DomainError(
                    "this participant was not claimed from a round-only golfer"
                )

            if (
                state["requires_confirmation"]
                and not confirm_actor_history
            ):
                return {
                    "round_id": round_uuid,
                    "participant_id": participant["id"],
                    "undone": False,
                    **state,
                }

            round_only_golfer_id = self._uuid(
                state["round_only_golfer_id"],
                "round_only_golfer_id",
            )
            cursor.execute(
                """
                SELECT id, display_name
                FROM golfers
                WHERE id = %s
                  AND username IS NULL
                  AND password_hash IS NULL
                  AND recovery_key_hash IS NULL
                  AND recovery_key IS NULL
                """,
                (round_only_golfer_id,),
            )
            round_only_golfer = cursor.fetchone()
            if not round_only_golfer:
                raise DomainError(
                    "the original round-only golfer is no longer available"
                )

            cursor.execute(
                """
                SELECT display_name
                FROM golfers
                WHERE id = %s
                """,
                (golfer_uuid,),
            )
            account = cursor.fetchone()

            cursor.execute(
                """
                UPDATE round_participants
                SET golfer_id = %s
                WHERE id = %s
                """,
                (round_only_golfer_id, participant["id"]),
            )

            self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=participant["id"],
                event_type="participant_claim_undone",
                data={
                    "player_participant_id": str(participant["id"]),
                    "account_golfer_id": str(golfer_uuid),
                    "account_display_name": (
                        account["display_name"] if account else None
                    ),
                    "display_name": round_only_golfer["display_name"],
                    "actions_after_claim": state["actions_after_claim"],
                },
                content_event_key="participant.claim_undone",
                presentation_context={
                    "mode": round_row["mode"],
                    "subject": round_only_golfer["display_name"],
                },
            )

            return {
                "round_id": round_uuid,
                "participant_id": participant["id"],
                "undone": True,
                "display_name": round_only_golfer["display_name"],
                "actions_after_claim": state["actions_after_claim"],
            }

    @staticmethod
    def _end_early_state_from_cursor(
        cursor: Any,
        round_id: UUID,
    ) -> dict[str, Any]:
        cursor.execute(
            """
            SELECT rp.id AS participant_id, g.display_name
            FROM round_participants rp
            JOIN golfers g ON g.id = rp.golfer_id
            WHERE rp.round_id = %s
              AND rp.role = 'player'
              AND rp.participation_state = 'active'
              AND EXISTS (
                  SELECT 1
                  FROM auth_sessions session
                  WHERE session.golfer_id = rp.golfer_id
                    AND session.revoked_at IS NULL
                    AND session.expires_at > now()
                    AND session.last_seen_at >= now() - interval '30 minutes'
              )
            ORDER BY rp.joined_at, rp.id
            """,
            (round_id,),
        )
        eligible = cursor.fetchall()

        cursor.execute(
            """
            SELECT participant_id, vote, updated_at
            FROM round_end_early_votes
            WHERE round_id = %s
            ORDER BY updated_at, participant_id
            """,
            (round_id,),
        )
        vote_rows = cursor.fetchall()
        votes = {
            str(row["participant_id"]): bool(row["vote"])
            for row in vote_rows
        }

        eligible_rows = [
            {
                "participant_id": row["participant_id"],
                "display_name": row["display_name"],
                "vote": votes.get(str(row["participant_id"])),
            }
            for row in eligible
        ]
        yes_count = sum(
            1 for row in eligible_rows if row["vote"] is True
        )
        required_count = len(eligible_rows)
        return {
            "proposal_active": bool(vote_rows),
            "required_count": required_count,
            "yes_count": yes_count,
            "eligible": eligible_rows,
            "unanimous": (
                required_count > 0
                and yes_count == required_count
            ),
        }

    def set_end_early_vote(
        self,
        golfer_id: object,
        round_id: object,
        vote: object,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        if not isinstance(vote, bool):
            raise DomainError("end-early vote must be true or false")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            participant = self._participant(cursor, round_uuid, golfer_uuid)
            self._require_active_player(
                participant,
                "vote to end the round early",
            )
            require_active_round(
                round_row["status"],
                "vote to end the round early",
            )

            cursor.execute(
                """
                INSERT INTO round_end_early_votes (
                    round_id, participant_id, vote, updated_at
                )
                VALUES (%s, %s, %s, now())
                ON CONFLICT (round_id, participant_id)
                DO UPDATE SET vote = EXCLUDED.vote,
                              updated_at = now()
                """,
                (round_uuid, participant["id"], vote),
            )

            self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=participant["id"],
                event_type="round_end_early_vote",
                route_position=int(round_row["current_route_position"]),
                hole_number=int(round_row["current_hole"]),
                data={"vote": vote},
                content_event_key=(
                    "round.end_early.vote_yes"
                    if vote
                    else "round.end_early.vote_no"
                ),
                presentation_context={
                    "mode": round_row["mode"],
                    "hole": int(round_row["current_hole"]),
                },
            )

            state = self._end_early_state_from_cursor(
                cursor,
                round_uuid,
            )
            if not state["unanimous"]:
                return {
                    "round_id": round_uuid,
                    "status": "active",
                    "end_early": state,
                }

            cursor.execute(
                """
                UPDATE rounds
                SET status = 'completed',
                    end_reason = 'ended_early',
                    updated_at = now()
                WHERE id = %s
                """,
                (round_uuid,),
            )
            self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=participant["id"],
                event_type="round_end_early_completed",
                route_position=int(round_row["current_route_position"]),
                hole_number=int(round_row["current_hole"]),
                data={
                    "yes_count": state["yes_count"],
                    "required_count": state["required_count"],
                },
                content_event_key="round.ended_early",
                presentation_context={
                    "mode": round_row["mode"],
                    "hole": int(round_row["current_hole"]),
                },
            )
            return {
                "round_id": round_uuid,
                "status": "completed",
                "end_reason": "ended_early",
                "end_early": state,
                "results": self._round_results_from_cursor(
                    cursor,
                    round_uuid,
                    mode=round_row["mode"],
                    hole_count=round_row["hole_count"],
                ),
            }

    def get_round(
        self,
        golfer_id: object,
        code: object | None = None,
        *,
        round_id: object | None = None,
        event_limit: int | None = 100,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_code = str(code or "").strip()
        with self._connection() as connection, connection.cursor() as cursor:
            if round_id is not None:
                requested_round_id = self._uuid(round_id, "round_id")
                cursor.execute(
                    "SELECT id FROM rounds WHERE id = %s",
                    (requested_round_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT r.id
                    FROM rounds r
                    JOIN round_participants rp
                      ON rp.round_id = r.id
                     AND rp.golfer_id = %s
                    WHERE r.active_code = %s
                      AND r.status IN ('setup', 'active', 'completed')
                    ORDER BY
                        CASE r.status
                            WHEN 'setup' THEN 0
                            WHEN 'active' THEN 1
                            ELSE 2
                        END,
                        r.updated_at DESC
                    LIMIT 1
                    """,
                    (golfer_uuid, round_code),
                )
            found = cursor.fetchone()
            if not found:
                raise NotFound("round not found")
            round_row = self._round(cursor, found["id"])
            participant = self._participant(cursor, found["id"], golfer_uuid)
            cursor.execute(
                """
                SELECT rp.id, rp.role, rp.tee_name, rp.joined_at,
                       rp.participation_state, rp.tracked_from_position,
                       g.id AS golfer_id, g.display_name,
                       (
                           g.username IS NULL
                           AND g.password_hash IS NULL
                           AND g.recovery_key_hash IS NULL
                           AND g.recovery_key IS NULL
                       ) AS round_only
                FROM round_participants rp JOIN golfers g ON g.id = rp.golfer_id
                WHERE rp.round_id = %s ORDER BY rp.joined_at, rp.id
                """,
                (found["id"],),
            )
            round_row["participants"] = cursor.fetchall()

            cursor.execute(
                """
                SELECT route_position, hole_number, state, skip_reason
                FROM round_route_positions
                WHERE round_id = %s
                ORDER BY route_position
                """,
                (found["id"],),
            )
            round_row["route"] = cursor.fetchall()

            if round_row["course_id"]:
                cursor.execute(
                    """
                    SELECT id, external_course_id, name, cached_at
                    FROM cached_courses
                    WHERE id = %s
                    """,
                    (round_row["course_id"],),
                )
                round_row["course"] = cursor.fetchone()
                cursor.execute(
                    """
                    SELECT tee_name,
                           count(*) AS holes_with_tee,
                           sum(yardage) FILTER (WHERE yardage IS NOT NULL) AS total_yardage
                    FROM cached_course_hole_tees tees
                    JOIN (
                        SELECT DISTINCT hole_number
                        FROM round_route_positions
                        WHERE round_id = %s
                    ) route_holes
                      ON route_holes.hole_number = tees.hole_number
                    WHERE tees.course_id = %s
                    GROUP BY tee_name
                    ORDER BY max(yardage) DESC NULLS LAST, tee_name
                    """,
                    (found["id"], round_row["course_id"]),
                )
                round_row["available_tees"] = cursor.fetchall()
            else:
                round_row["course"] = None
                round_row["available_tees"] = []

            cursor.execute(
                """
                SELECT rp.route_position, rr.hole_number, rp.par, rp.source
                FROM round_route_pars rp
                JOIN round_route_positions rr
                  ON rr.round_id = rp.round_id
                 AND rr.route_position = rp.route_position
                WHERE rp.round_id = %s
                ORDER BY rp.route_position
                """,
                (found["id"],),
            )
            round_row["pars"] = cursor.fetchall()
            cursor.execute(
                """
                SELECT id, route_position, hole_number, score_scope,
                       player_participant_id, strokes, updated_at
                FROM round_hole_scores
                WHERE round_id = %s
                ORDER BY route_position, player_participant_id NULLS FIRST
                """,
                (found["id"],),
            )
            round_row["scores"] = cursor.fetchall()
            cursor.execute(
                """
                SELECT route_position, hole_number, shot_type,
                       player_participant_id, updated_at
                FROM scramble_contributions
                WHERE round_id = %s
                ORDER BY route_position, shot_type
                """,
                (found["id"],),
            )
            round_row["contributions"] = cursor.fetchall()
            round_row["results"] = self._round_results_from_cursor(
                cursor,
                found["id"],
                mode=round_row["mode"],
                hole_count=round_row["hole_count"],
            )
            event_query = """
                SELECT id, actor_participant_id, event_type, hole_number,
                       route_position, old_value, new_value, data, reply_to_event_id,
                       content_event_key, presentation, created_at
                FROM round_events
                WHERE round_id = %s
                ORDER BY created_at DESC, id DESC
            """
            event_params: list[object] = [found["id"]]
            if event_limit is not None:
                event_query += " LIMIT %s"
                event_params.append(max(1, int(event_limit)))
            cursor.execute(event_query, tuple(event_params))
            events = cursor.fetchall()
            catalog = ContentCatalog.load()
            preferences = self._preferences_from_cursor(
                cursor,
                golfer_uuid,
                catalog,
            )
            for event in events:
                raw_presentation = event.get("presentation") or {}
                variants = dict(raw_presentation.get("variants") or {})
                audience = "everyone"
                event_data = event.get("data") or {}

                subject_id = event_data.get("player_participant_id")
                target_id = event_data.get("target_participant_id")
                viewer_participant_id = str(participant["id"])

                if (
                    subject_id is not None
                    and str(subject_id) == viewer_participant_id
                    and "subject" in variants
                ):
                    audience = "subject"
                elif (
                    subject_id is not None
                    and str(subject_id) != viewer_participant_id
                    and "others" in variants
                ):
                    audience = "others"
                elif (
                    target_id is not None
                    and str(target_id) == viewer_participant_id
                    and "target" in variants
                ):
                    audience = "target"
                elif (
                    event.get("actor_participant_id") == participant["id"]
                    and "actor" in variants
                ):
                    audience = "actor"
                elif participant["role"] == "player" and "team" in variants:
                    audience = "team"

                event["presentation"] = filter_presentation_for_preferences(
                    raw_presentation,
                    preferences,
                    audience=audience,
                )

            round_row["events"] = events

            cursor.execute(
                """
                SELECT reactions.event_id, reactions.actor_participant_id,
                       reactions.reaction_kind, reactions.updated_at
                FROM round_event_reactions reactions
                JOIN round_events event
                  ON event.id = reactions.event_id
                WHERE event.round_id = %s
                ORDER BY reactions.updated_at, reactions.actor_participant_id
                """,
                (found["id"],),
            )
            round_row["reactions"] = cursor.fetchall()

            cursor.execute(
                """
                SELECT challenges.score_event_id,
                       challenges.challenger_participant_id,
                       challenges.proposed_score, challenges.comment,
                       challenges.status, challenges.created_at,
                       challenges.updated_at
                FROM score_challenges challenges
                JOIN round_events event
                  ON event.id = challenges.score_event_id
                WHERE event.round_id = %s
                ORDER BY challenges.updated_at, challenges.challenger_participant_id
                """,
                (found["id"],),
            )
            round_row["score_challenges"] = cursor.fetchall()

            round_row["end_early"] = self._end_early_state_from_cursor(
                cursor,
                found["id"],
            )
            round_row["claim_undo"] = (
                self._claim_undo_state_from_cursor(
                    cursor,
                    found["id"],
                    participant["id"],
                )
                if round_row["status"] == "active"
                else None
            )
            round_row["viewer_role"] = participant["role"]
            round_row["viewer_participant_id"] = participant["id"]
            return round_row

    def set_current_hole(
        self,
        golfer_id: object,
        round_id: object,
        hole: object,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            participant = self._participant(
                cursor,
                round_uuid,
                golfer_uuid,
            )
            self._require_active_player(
                participant,
                "change the current hole",
            )
            require_active_round(
                round_row["status"],
                "change the current hole",
            )

            route_row = self._route_position(
                cursor,
                round_uuid,
                hole,
                lock=True,
            )
            new_position = int(route_row["route_position"])
            old_position = int(round_row["current_route_position"])

            validate_shared_hole_change(
                old_position,
                new_position,
            )
            if new_position > old_position + 1:
                raise DomainError(
                    "shared active hole can only advance one route position at a time"
                )

            if new_position != old_position:
                old_hole = int(round_row["current_hole"])
                new_hole = int(route_row["hole_number"])
                cursor.execute(
                    """
                    UPDATE rounds
                    SET current_route_position = %s,
                        current_hole = %s,
                        updated_at = now()
                    WHERE id = %s
                    """,
                    (new_position, new_hole, round_uuid),
                )
                self._event(
                    cursor,
                    round_id=round_uuid,
                    actor_participant_id=participant["id"],
                    event_type="current_hole_change",
                    hole_number=new_hole,
                    route_position=new_position,
                    old_value={
                        "route_position": old_position,
                        "hole_number": old_hole,
                    },
                    new_value={
                        "route_position": new_position,
                        "hole_number": new_hole,
                    },
                    content_event_key="hole.advance",
                    presentation_context={
                        "hole": new_hole,
                        "mode": round_row["mode"],
                    },
                )

            return {
                "round_id": round_uuid,
                "current_hole": int(route_row["hole_number"]),
                "current_route_position": new_position,
            }

    def _maybe_advance_active_route(
        self,
        cursor: Any,
        *,
        round_row: dict[str, Any],
        actor_participant_id: UUID,
        scored_route_position: int,
    ) -> dict[str, int] | None:
        current_position = int(round_row["current_route_position"])
        if scored_route_position != current_position:
            return None

        if round_row["mode"] == "scramble":
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM round_hole_scores
                    WHERE round_id = %s
                      AND route_position = %s
                      AND score_scope = 'team'
                ) AS complete
                """,
                (round_row["id"], current_position),
            )
            complete = bool(cursor.fetchone()["complete"])
        else:
            cursor.execute(
                """
                SELECT
                    count(prp.participant_id)
                        FILTER (
                            WHERE rp.participation_state = 'active'
                        ) AS required_players,
                    count(s.id)
                        FILTER (
                            WHERE rp.participation_state = 'active'
                        ) AS scored_players
                FROM round_participant_route_positions prp
                JOIN round_participants rp
                  ON rp.id = prp.participant_id
                 AND rp.round_id = prp.round_id
                 AND rp.role = 'player'
                LEFT JOIN round_hole_scores s
                  ON s.round_id = prp.round_id
                 AND s.route_position = prp.route_position
                 AND s.player_participant_id = prp.participant_id
                 AND s.score_scope = 'player'
                WHERE prp.round_id = %s
                  AND prp.route_position = %s
                  AND prp.required
                """,
                (round_row["id"], current_position),
            )
            counts = cursor.fetchone()
            required_players = int(counts["required_players"] or 0)
            scored_players = int(counts["scored_players"] or 0)
            complete = (
                required_players > 0
                and scored_players >= required_players
            )

        if not complete:
            return None

        cursor.execute(
            """
            SELECT route_position, hole_number
            FROM round_route_positions
            WHERE round_id = %s
              AND route_position > %s
              AND state = 'planned'
            ORDER BY route_position
            LIMIT 1
            """,
            (round_row["id"], current_position),
        )
        next_route = cursor.fetchone()
        if not next_route:
            return None

        next_position = int(next_route["route_position"])
        next_hole = int(next_route["hole_number"])
        cursor.execute(
            """
            UPDATE rounds
            SET current_route_position = %s,
                current_hole = %s,
                updated_at = now()
            WHERE id = %s
            """,
            (
                next_position,
                next_hole,
                round_row["id"],
            ),
        )
        self._event(
            cursor,
            round_id=round_row["id"],
            actor_participant_id=actor_participant_id,
            event_type="current_hole_auto_advance",
            hole_number=next_hole,
            route_position=next_position,
            old_value={
                "route_position": current_position,
                "hole_number": int(round_row["current_hole"]),
            },
            new_value={
                "route_position": next_position,
                "hole_number": next_hole,
            },
            content_event_key="hole.advance",
            presentation_context={
                "hole": next_hole,
                "mode": round_row["mode"],
            },
        )
        return {
            "current_route_position": next_position,
            "current_hole": next_hole,
        }

    @staticmethod
    def _round_results_from_cursor(
        cursor: Any,
        round_id: UUID,
        *,
        mode: str,
        hole_count: int,
    ) -> dict[str, Any]:
        cursor.execute(
            """
            SELECT count(*) AS required_count
            FROM round_route_positions
            WHERE round_id = %s
              AND state = 'planned'
            """,
            (round_id,),
        )
        route_required = int(cursor.fetchone()["required_count"])

        if mode == "scramble":
            cursor.execute(
                """
                SELECT count(s.id) AS score_count,
                       coalesce(sum(s.strokes), 0) AS total_strokes
                FROM round_route_positions rr
                LEFT JOIN round_hole_scores s
                  ON s.round_id = rr.round_id
                 AND s.route_position = rr.route_position
                 AND s.score_scope = 'team'
                WHERE rr.round_id = %s
                  AND rr.state = 'planned'
                """,
                (round_id,),
            )
            row = cursor.fetchone()
            score_count = int(row["score_count"])
            return {
                "mode": "scramble",
                "complete": score_count == route_required,
                "coverage_state": (
                    "complete"
                    if score_count == route_required
                    else "incomplete"
                ),
                "score_count": score_count,
                "required_scores": route_required,
                "missing_scores": max(route_required - score_count, 0),
                "team_total": (
                    int(row["total_strokes"])
                    if score_count
                    else None
                ),
                "players": [],
            }

        cursor.execute(
            """
            SELECT rp.id AS participant_id,
                   g.display_name,
                   rp.participation_state,
                   rp.tracked_from_position,
                   count(prp.route_position)
                     FILTER (
                         WHERE prp.required
                           AND rr.route_position IS NOT NULL
                     ) AS required_count,
                   count(s.id) AS score_count,
                   coalesce(sum(s.strokes), 0) AS total_strokes
            FROM round_participants rp
            JOIN golfers g
              ON g.id = rp.golfer_id
            LEFT JOIN round_participant_route_positions prp
              ON prp.round_id = rp.round_id
             AND prp.participant_id = rp.id
             AND prp.required
            LEFT JOIN round_route_positions rr
              ON rr.round_id = prp.round_id
             AND rr.route_position = prp.route_position
             AND rr.state = 'planned'
            LEFT JOIN round_hole_scores s
              ON s.round_id = rp.round_id
             AND s.route_position = prp.route_position
             AND s.player_participant_id = rp.id
             AND s.score_scope = 'player'
             AND rr.route_position IS NOT NULL
            WHERE rp.round_id = %s
              AND rp.role = 'player'
              AND rp.participation_state <> 'removed'
            GROUP BY rp.id, g.display_name, rp.joined_at,
                     rp.participation_state, rp.tracked_from_position
            ORDER BY rp.joined_at, rp.id
            """,
            (round_id,),
        )
        players = cursor.fetchall()
        results: list[dict[str, Any]] = []

        for row in players:
            required_count = int(row["required_count"] or 0)
            score_count = int(row["score_count"] or 0)
            participation_state = str(
                row["participation_state"] or "active"
            )
            is_partial = (
                int(row["tracked_from_position"] or 1) > 1
                or required_count < route_required
            )
            if score_count < required_count:
                coverage_state = "incomplete"
            elif is_partial:
                coverage_state = "partial"
            else:
                coverage_state = "complete"

            placement_eligible = (
                participation_state == "active"
                and coverage_state == "complete"
                and required_count == route_required
            )

            results.append(
                {
                    "participant_id": row["participant_id"],
                    "display_name": row["display_name"],
                    "participation_state": participation_state,
                    "coverage_state": coverage_state,
                    "placement_eligible": placement_eligible,
                    "tracked_from_position": int(
                        row["tracked_from_position"] or 1
                    ),
                    "required_scores": required_count,
                    "score_count": score_count,
                    "missing_scores": max(
                        required_count - score_count,
                        0,
                    ),
                    "total_strokes": (
                        int(row["total_strokes"])
                        if score_count
                        else None
                    ),
                    "rank": None,
                    "tie_count": 0,
                }
            )

        eligible = [
            row
            for row in results
            if row["placement_eligible"]
            and row["total_strokes"] is not None
        ]

        if eligible:
            for row in eligible:
                total = int(row["total_strokes"])
                row["rank"] = 1 + sum(
                    1
                    for candidate in eligible
                    if int(candidate["total_strokes"]) < total
                )
                row["tie_count"] = sum(
                    1
                    for candidate in eligible
                    if int(candidate["total_strokes"]) == total
                )

        active_results = [
            row
            for row in results
            if row["participation_state"] == "active"
        ]
        complete = bool(active_results) and all(
            row["missing_scores"] == 0
            for row in active_results
        )

        return {
            "mode": "individual",
            "complete": complete,
            "score_count": sum(
                int(row["score_count"])
                for row in results
            ),
            "missing_scores": sum(
                int(row["missing_scores"])
                for row in active_results
            ),
            "team_total": None,
            "players": results,
        }

    @staticmethod
    def _individual_round_end_event(
        result: dict[str, Any],
        results: list[dict[str, Any]],
    ) -> str:
        rank = int(result["rank"])
        tie_count = int(result["tie_count"])
        player_count = len(results)

        if rank == 1:
            return (
                "round.end.individual.co_winner"
                if tie_count > 1
                else "round.end.individual.winner"
            )

        if player_count == 2:
            return "round.end.individual.head_to_head_loser"

        max_total = max(int(row["total_strokes"]) for row in results)
        if int(result["total_strokes"]) == max_total:
            return (
                "round.end.individual.tied_last"
                if tie_count > 1
                else "round.end.individual.dead_last"
            )

        if tie_count > 1:
            return "round.end.individual.tied_middle"

        return "round.end.individual.not_last"

    def set_status(
        self,
        golfer_id: object,
        round_id: object,
        status: object,
        *,
        finish_incomplete: bool = False,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        new_status = str(status or "")
        if new_status not in ROUND_STATUSES:
            raise DomainError("unsupported round status")
        transitions = {
            "setup": {"active", "abandoned"},
            "active": {"completed", "abandoned"},
            "completed": {"active"},
            "abandoned": {"active"},
        }
        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            participant = self._participant(cursor, round_uuid, golfer_uuid)
            self._require_active_player(participant, "change round status")
            old_status = round_row["status"]
            if new_status != old_status:
                if new_status not in transitions[old_status]:
                    raise DomainError(f"cannot change round from {old_status} to {new_status}")

                if (
                    old_status == "setup"
                    and new_status == "active"
                    and round_row["course_id"]
                ):
                    cursor.execute(
                        """
                        SELECT EXISTS (
                            SELECT 1
                            FROM cached_course_hole_tees
                            WHERE course_id = %s
                        ) AS has_tees
                        """,
                        (round_row["course_id"],),
                    )
                    has_tees = bool(cursor.fetchone()["has_tees"])
                    if has_tees:
                        if round_row["mode"] == "scramble":
                            if not round_row.get("scramble_tee_name"):
                                raise DomainError(
                                    "choose one team scoring tee before starting"
                                )
                        else:
                            cursor.execute(
                                """
                                SELECT count(*) AS missing
                                FROM round_participants
                                WHERE round_id = %s
                                  AND role = 'player'
                                  AND tee_name IS NULL
                                """,
                                (round_uuid,),
                            )
                            if int(cursor.fetchone()["missing"]) > 0:
                                raise DomainError(
                                    "every player must choose a tee before starting"
                                )

                completion_results: dict[str, Any] | None = None
                completion_incomplete = False
                if old_status == "active" and new_status == "completed":
                    completion_results = self._round_results_from_cursor(
                        cursor,
                        round_uuid,
                        mode=round_row["mode"],
                        hole_count=round_row["hole_count"],
                    )
                    completion_incomplete = not completion_results["complete"]
                    if completion_incomplete:
                        if not finish_incomplete:
                            if round_row["mode"] == "scramble":
                                raise DomainError(
                                    "team scores are missing; explicitly finish incomplete or fix the scorecard"
                                )
                            raise DomainError(
                                "player scores are missing; explicitly finish incomplete or fix the scorecard"
                            )

                        cursor.execute(
                            """
                            SELECT max(route_position) AS final_position
                            FROM round_route_positions
                            WHERE round_id = %s AND state = 'planned'
                            """,
                            (round_uuid,),
                        )
                        final_position = int(
                            cursor.fetchone()["final_position"]
                            or round_row["current_route_position"]
                        )
                        if int(round_row["current_route_position"]) != final_position:
                            raise DomainError(
                                "finish incomplete is only available at the final route position"
                            )

                cursor.execute(
                    "UPDATE rounds SET status = %s, updated_at = now() WHERE id = %s",
                    (new_status, round_uuid),
                )
                content_event = (
                    None
                    if completion_incomplete
                    else status_content_event(old_status, new_status)
                )
                self._event(
                    cursor,
                    round_id=round_uuid,
                    actor_participant_id=participant["id"],
                    event_type="round_status_change",
                    old_value=old_status,
                    new_value=new_status,
                    data=(
                        {
                            "finish_incomplete": True,
                            "missing_scores": completion_results["missing_scores"],
                        }
                        if completion_incomplete and completion_results is not None
                        else {}
                    ),
                    content_event_key=content_event,
                    presentation_context={"mode": round_row["mode"]},
                )

                if completion_results is not None:
                    if round_row["mode"] == "scramble":
                        if completion_results["complete"]:
                            self._event(
                                cursor,
                                round_id=round_uuid,
                                actor_participant_id=participant["id"],
                                event_type="round_end_result",
                                data={
                                    "mode": "scramble",
                                    "total_strokes": completion_results["team_total"],
                                },
                                content_event_key="round.end.scramble.complete",
                                presentation_context={
                                    "mode": "scramble",
                                    "strokes": completion_results["team_total"],
                                },
                            )
                    else:
                        placement_results = [
                            row
                            for row in completion_results["players"]
                            if row.get("rank") is not None
                        ]
                        for result in placement_results:
                            event_key = self._individual_round_end_event(
                                result,
                                placement_results,
                            )
                            self._event(
                                cursor,
                                round_id=round_uuid,
                                actor_participant_id=participant["id"],
                                event_type="round_end_result",
                                data={
                                    "mode": "individual",
                                    "player_participant_id": str(
                                        result["participant_id"]
                                    ),
                                    "display_name": result["display_name"],
                                    "rank": result["rank"],
                                    "tie_count": result["tie_count"],
                                    "total_strokes": result["total_strokes"],
                                },
                                content_event_key=event_key,
                                presentation_context={
                                    "mode": "individual",
                                    "strokes": result["total_strokes"],
                                },
                            )

            response = {"round_id": round_uuid, "status": new_status}
            if new_status == "completed":
                response["results"] = self._round_results_from_cursor(
                    cursor,
                    round_uuid,
                    mode=round_row["mode"],
                    hole_count=round_row["hole_count"],
                )
            return response

    def set_par(
        self,
        golfer_id: object,
        round_id: object,
        hole: object,
        par: object,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        try:
            par_value = int(par)
        except (TypeError, ValueError) as error:
            raise DomainError("par must be between 2 and 7") from error
        if not 2 <= par_value <= 7:
            raise DomainError("par must be between 2 and 7")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid)
            participant = self._participant(
                cursor,
                round_uuid,
                golfer_uuid,
            )
            self._require_active_player(participant, "change par")
            if round_row["status"] not in {"setup", "active"}:
                raise DomainError(
                    "par can only be changed before or during an active round"
                )
            if not bool(round_row["par_tracking_enabled"]):
                raise DomainError("par tracking is disabled for this round")

            route_row = self._route_position(
                cursor,
                round_uuid,
                hole,
                lock=True,
            )
            route_position = int(route_row["route_position"])
            hole_number = int(route_row["hole_number"])

            cursor.execute(
                """
                SELECT par
                FROM round_route_pars
                WHERE round_id = %s
                  AND route_position = %s
                FOR UPDATE
                """,
                (round_uuid, route_position),
            )
            previous = cursor.fetchone()
            old_par = previous["par"] if previous else None
            if old_par == par_value:
                return {
                    "round_id": round_uuid,
                    "route_position": route_position,
                    "hole": hole_number,
                    "par": par_value,
                    "event": None,
                }

            cursor.execute(
                """
                INSERT INTO round_route_pars (
                    round_id, route_position, par, source
                )
                VALUES (%s, %s, %s, 'manual')
                ON CONFLICT (round_id, route_position)
                DO UPDATE SET
                    par = EXCLUDED.par,
                    source = 'manual',
                    updated_at = now()
                """,
                (round_uuid, route_position, par_value),
            )

            event = self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=participant["id"],
                event_type=audit_event_type("par", old_par),
                hole_number=hole_number,
                route_position=route_position,
                old_value=old_par,
                new_value=par_value,
                content_event_key=par_content_event(
                    old_par,
                    par_value,
                ),
                presentation_context={
                    "hole": hole_number,
                    "par": par_value,
                    "mode": round_row["mode"],
                },
            )
            return {
                "round_id": round_uuid,
                "route_position": route_position,
                "hole": hole_number,
                "par": par_value,
                "event": event,
            }

    @staticmethod
    def _score_series_from_cursor(
        cursor: Any,
        round_id: UUID,
        *,
        scope: str,
        participant_id: UUID | None,
    ) -> list[dict[str, Any]]:
        cursor.execute(
            """
            SELECT s.route_position AS hole_number, s.strokes, p.par
            FROM round_hole_scores s
            LEFT JOIN round_route_pars p
              ON p.round_id = s.round_id
             AND p.route_position = s.route_position
            WHERE s.round_id = %s
              AND s.score_scope = %s
              AND s.player_participant_id IS NOT DISTINCT FROM %s
            ORDER BY s.route_position
            """,
            (round_id, scope, participant_id),
        )
        return cursor.fetchall()

    @staticmethod
    def _individual_standing_state_from_cursor(
        cursor: Any,
        round_id: UUID,
        *,
        hole_count: int,
    ) -> dict[str, Any] | None:
        cursor.execute(
            """
            SELECT rp.id AS participant_id, g.display_name
            FROM round_participants rp
            JOIN golfers g ON g.id = rp.golfer_id
            WHERE rp.round_id = %s
              AND rp.role = 'player'
              AND rp.participation_state = 'active'
              AND rp.tracked_from_position = 1
            ORDER BY rp.joined_at, rp.id
            """,
            (round_id,),
        )
        players = cursor.fetchall()
        if len(players) < 2:
            return None

        participant_ids = [row["participant_id"] for row in players]
        names = {
            str(row["participant_id"]): row["display_name"]
            for row in players
        }

        cursor.execute(
            """
            SELECT player_participant_id, route_position, strokes
            FROM round_hole_scores
            WHERE round_id = %s
              AND score_scope = 'player'
            ORDER BY route_position, player_participant_id
            """,
            (round_id,),
        )
        score_rows = cursor.fetchall()

        scores: dict[UUID, dict[int, int]] = {
            participant_id: {}
            for participant_id in participant_ids
        }
        for row in score_rows:
            participant_id = row["player_participant_id"]
            if participant_id in scores:
                scores[participant_id][int(row["route_position"])] = int(
                    row["strokes"]
                )

        through_hole = 0
        for hole in range(1, int(hole_count) + 1):
            if all(hole in scores[participant_id] for participant_id in participant_ids):
                through_hole = hole
            else:
                break

        if through_hole == 0:
            return None

        totals = {
            str(participant_id): sum(
                scores[participant_id][hole]
                for hole in range(1, through_hole + 1)
            )
            for participant_id in participant_ids
        }
        minimum = min(totals.values())
        maximum = max(totals.values())

        return {
            "through_hole": through_hole,
            "player_count": len(participant_ids),
            "totals": totals,
            "leaders": {
                participant_id
                for participant_id, total in totals.items()
                if total == minimum
            },
            "last": {
                participant_id
                for participant_id, total in totals.items()
                if total == maximum
            },
            "names": names,
        }

    @staticmethod
    def _derived_event_exists(
        cursor: Any,
        round_id: UUID,
        event_key: str,
        *,
        participant_id: UUID | None,
    ) -> bool:
        if participant_id is None:
            cursor.execute(
                """
                SELECT 1
                FROM round_events
                WHERE round_id = %s
                  AND content_event_key = %s
                LIMIT 1
                """,
                (round_id, event_key),
            )
        else:
            cursor.execute(
                """
                SELECT 1
                FROM round_events
                WHERE round_id = %s
                  AND content_event_key = %s
                  AND data->>'player_participant_id' = %s
                LIMIT 1
                """,
                (round_id, event_key, str(participant_id)),
            )
        return cursor.fetchone() is not None

    def set_score(
        self,
        golfer_id: object,
        round_id: object,
        hole: object,
        strokes: object,
        *,
        player_participant_id: object | None = None,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        try:
            stroke_value = int(strokes)
        except (TypeError, ValueError) as error:
            raise DomainError("strokes must be between 1 and 99") from error
        if not 1 <= stroke_value <= 99:
            raise DomainError("strokes must be between 1 and 99")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            actor = self._participant(
                cursor,
                round_uuid,
                golfer_uuid,
            )
            self._require_active_player(actor, "change scores")
            require_active_round(round_row["status"], "change scores")

            route_row = self._route_position(
                cursor,
                round_uuid,
                hole,
                lock=True,
            )
            route_position = int(route_row["route_position"])
            hole_number = int(route_row["hole_number"])

            if route_row["state"] != "planned":
                raise DomainError("cannot score a skipped route position")
            if route_position > int(round_row["current_route_position"]):
                raise DomainError(
                    "future holes are preview-only until they become active"
                )

            if round_row["mode"] == "individual":
                target_id = self._uuid(
                    player_participant_id,
                    "player_participant_id",
                )
                cursor.execute(
                    """
                    SELECT rp.role, rp.participation_state,
                           rp.tracked_from_position, g.display_name
                    FROM round_participants rp
                    JOIN golfers g ON g.id = rp.golfer_id
                    WHERE rp.id = %s AND rp.round_id = %s
                    """,
                    (target_id, round_uuid),
                )
                target = cursor.fetchone()
                if not target or target["role"] != "player":
                    raise DomainError(
                        "score target must be a player in this round"
                    )
                scope = "player"
                subject_name = target["display_name"]
                if (
                    target["participation_state"] != "active"
                    and route_position >= int(round_row["current_route_position"])
                ):
                    raise DomainError(
                        "withdrawn players can only backfill earlier scores until they return"
                    )

                cursor.execute(
                    """
                    INSERT INTO round_participant_route_positions (
                        round_id, participant_id, route_position, required
                    )
                    VALUES (%s, %s, %s, true)
                    ON CONFLICT (participant_id, route_position)
                    DO UPDATE SET required = true
                    """,
                    (round_uuid, target_id, route_position),
                )
                if route_position < int(
                    target["tracked_from_position"] or route_position
                ):
                    cursor.execute(
                        """
                        UPDATE round_participants
                        SET tracked_from_position = %s
                        WHERE id = %s
                        """,
                        (route_position, target_id),
                    )
            else:
                if player_participant_id is not None:
                    raise DomainError(
                        "scramble rounds use one team score"
                    )
                target_id = None
                scope = "team"
                subject_name = "Team"

            before_series = self._score_series_from_cursor(
                cursor,
                round_uuid,
                scope=scope,
                participant_id=target_id,
            )
            before_standings = (
                self._individual_standing_state_from_cursor(
                    cursor,
                    round_uuid,
                    hole_count=round_row["hole_count"],
                )
                if round_row["mode"] == "individual"
                else None
            )

            cursor.execute(
                """
                SELECT id, strokes
                FROM round_hole_scores
                WHERE round_id = %s
                  AND route_position = %s
                  AND score_scope = %s
                  AND player_participant_id IS NOT DISTINCT FROM %s
                FOR UPDATE
                """,
                (
                    round_uuid,
                    route_position,
                    scope,
                    target_id,
                ),
            )
            previous = cursor.fetchone()
            old_score = previous["strokes"] if previous else None
            if old_score == stroke_value:
                return {
                    "round_id": round_uuid,
                    "route_position": route_position,
                    "hole": hole_number,
                    "strokes": stroke_value,
                    "event": None,
                }

            if previous:
                cursor.execute(
                    """
                    UPDATE round_hole_scores
                    SET strokes = %s,
                        hole_number = %s,
                        updated_at = now()
                    WHERE id = %s
                    """,
                    (
                        stroke_value,
                        hole_number,
                        previous["id"],
                    ),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO round_hole_scores (
                        round_id, route_position, hole_number,
                        score_scope, player_participant_id, strokes
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        round_uuid,
                        route_position,
                        hole_number,
                        scope,
                        target_id,
                        stroke_value,
                    ),
                )

            cursor.execute(
                """
                SELECT par
                FROM round_route_pars
                WHERE round_id = %s
                  AND route_position = %s
                """,
                (round_uuid, route_position),
            )
            par_row = cursor.fetchone()
            par_value = par_row["par"] if par_row else None

            if (
                bool(round_row["par_tracking_enabled"])
                and par_value is None
            ):
                raise DomainError(
                    "establish par for this hole before entering a score"
                )

            after_series = self._score_series_from_cursor(
                cursor,
                round_uuid,
                scope=scope,
                participant_id=target_id,
            )
            after_standings = (
                self._individual_standing_state_from_cursor(
                    cursor,
                    round_uuid,
                    hole_count=round_row["hole_count"],
                )
                if round_row["mode"] == "individual"
                else None
            )

            is_backfill = (
                old_score is None
                and route_position
                < int(round_row["current_route_position"])
            )

            if not is_backfill:
                for derived_event in score_transition_events(
                    before_series,
                    after_series,
                ):
                    if (
                        derived_event
                        in {
                            "score.derived.first_birdie",
                            "score.derived.first_eagle",
                        }
                        and self._derived_event_exists(
                            cursor,
                            round_uuid,
                            derived_event,
                            participant_id=target_id,
                        )
                    ):
                        continue

                    self._event(
                        cursor,
                        round_id=round_uuid,
                        actor_participant_id=actor["id"],
                        event_type="score_derived",
                        hole_number=hole_number,
                        route_position=route_position,
                        data={
                            "scope": scope,
                            "player_participant_id": (
                                str(target_id)
                                if target_id
                                else None
                            ),
                        },
                        content_event_key=derived_event,
                        presentation_context={
                            "hole": hole_number,
                            "mode": round_row["mode"],
                            "subject": subject_name,
                        },
                    )

                for (
                    derived_event,
                    participant_id,
                ) in standing_transition_events(
                    before_standings,
                    after_standings,
                ):
                    standing_names = (
                        (after_standings or {}).get("names")
                        or (before_standings or {}).get("names")
                        or {}
                    )
                    standing_position = (
                        after_standings
                        or before_standings
                        or {}
                    ).get("through_hole")
                    physical_hole = hole_number
                    if standing_position:
                        standing_route = self._route_position(
                            cursor,
                            round_uuid,
                            standing_position,
                        )
                        physical_hole = int(
                            standing_route["hole_number"]
                        )

                    self._event(
                        cursor,
                        round_id=round_uuid,
                        actor_participant_id=actor["id"],
                        event_type="score_derived",
                        hole_number=physical_hole,
                        route_position=standing_position,
                        data={
                            "scope": "player",
                            "player_participant_id": participant_id,
                        },
                        content_event_key=derived_event,
                        presentation_context={
                            "hole": physical_hole,
                            "mode": "individual",
                            "subject": standing_names.get(
                                participant_id,
                                "Golfer",
                            ),
                        },
                    )

            auto_advance = self._maybe_advance_active_route(
                cursor,
                round_row=round_row,
                actor_participant_id=actor["id"],
                scored_route_position=route_position,
            )

            content_event = score_content_event(
                mode=round_row["mode"],
                old_score=old_score,
                new_score=stroke_value,
                par=par_value,
                hole_number=route_position,
                current_hole=int(
                    round_row["current_route_position"]
                ),
            )
            event = self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=actor["id"],
                event_type=audit_event_type("score", old_score),
                hole_number=hole_number,
                route_position=route_position,
                old_value=old_score,
                new_value=stroke_value,
                data={
                    "scope": scope,
                    "player_participant_id": (
                        str(target_id) if target_id else None
                    ),
                    "backfilled": is_backfill,
                },
                content_event_key=content_event,
                presentation_context={
                    "hole": hole_number,
                    "par": (
                        par_value
                        if par_value is not None
                        else ""
                    ),
                    "strokes": stroke_value,
                    "old_score": (
                        old_score if old_score is not None else ""
                    ),
                    "new_score": stroke_value,
                    "mode": round_row["mode"],
                    "score_name": content_event.rsplit(".", 1)[-1],
                },
            )

            response = {
                "round_id": round_uuid,
                "route_position": route_position,
                "hole": hole_number,
                "strokes": stroke_value,
                "event": event,
            }
            if auto_advance:
                response.update(auto_advance)
            return response

    def remove_score(
        self,
        golfer_id: object,
        round_id: object,
        hole: object,
        *,
        player_participant_id: object | None = None,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            actor = self._participant(
                cursor,
                round_uuid,
                golfer_uuid,
            )
            self._require_active_player(actor, "change scores")
            require_active_round(round_row["status"], "change scores")

            route_row = self._route_position(
                cursor,
                round_uuid,
                hole,
                lock=True,
            )
            route_position = int(route_row["route_position"])
            hole_number = int(route_row["hole_number"])

            if route_row["state"] != "planned":
                raise DomainError("cannot remove a score from a skipped route position")
            if route_position > int(round_row["current_route_position"]):
                raise DomainError(
                    "future holes are preview-only until they become active"
                )

            if round_row["mode"] == "individual":
                target_id = self._uuid(
                    player_participant_id,
                    "player_participant_id",
                )
                cursor.execute(
                    """
                    SELECT rp.role, g.display_name
                    FROM round_participants rp
                    JOIN golfers g ON g.id = rp.golfer_id
                    WHERE rp.id = %s AND rp.round_id = %s
                    """,
                    (target_id, round_uuid),
                )
                target = cursor.fetchone()
                if not target or target["role"] != "player":
                    raise DomainError(
                        "score target must be a player in this round"
                    )
                scope = "player"
                subject_name = target["display_name"]
            else:
                if player_participant_id is not None:
                    raise DomainError(
                        "scramble rounds use one team score"
                    )
                target_id = None
                scope = "team"
                subject_name = "Team"

            cursor.execute(
                """
                SELECT id, strokes
                FROM round_hole_scores
                WHERE round_id = %s
                  AND route_position = %s
                  AND score_scope = %s
                  AND player_participant_id IS NOT DISTINCT FROM %s
                FOR UPDATE
                """,
                (
                    round_uuid,
                    route_position,
                    scope,
                    target_id,
                ),
            )
            score = cursor.fetchone()
            if not score:
                raise DomainError("there is no score to remove")

            old_score = int(score["strokes"])
            cursor.execute(
                "DELETE FROM round_hole_scores WHERE id = %s",
                (score["id"],),
            )

            event = self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=actor["id"],
                event_type="score_removed",
                hole_number=hole_number,
                route_position=route_position,
                old_value=old_score,
                new_value=None,
                data={
                    "scope": scope,
                    "player_participant_id": (
                        str(target_id) if target_id else None
                    ),
                    "subject": subject_name,
                },
                content_event_key="score.removed",
                presentation_context={
                    "hole": hole_number,
                    "mode": round_row["mode"],
                    "subject": subject_name,
                    "old_score": old_score,
                },
            )

            return {
                "round_id": round_uuid,
                "route_position": route_position,
                "hole": hole_number,
                "removed_strokes": old_score,
                "event": event,
            }

    def set_scramble_contribution(
        self,
        golfer_id: object,
        round_id: object,
        hole: object,
        shot_type: object,
        player_participant_id: object | None,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        normalized_type = normalize_shot_type(shot_type)
        target_id = (
            self._uuid(
                player_participant_id,
                "player_participant_id",
            )
            if player_participant_id is not None
            else None
        )

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid)
            actor = self._participant(
                cursor,
                round_uuid,
                golfer_uuid,
            )
            self._require_active_player(actor, "change contributions")
            if round_row["status"] != "active":
                raise DomainError(
                    "contributions are only available during an active round"
                )
            if round_row["mode"] != "scramble":
                raise DomainError(
                    "contributions are only available for scramble rounds"
                )

            route_row = self._route_position(
                cursor,
                round_uuid,
                hole,
                lock=True,
            )
            route_position = int(route_row["route_position"])
            hole_number = int(route_row["hole_number"])

            if route_position > int(round_row["current_route_position"]):
                raise DomainError(
                    "future holes are preview-only until they become active"
                )
            if route_row["state"] != "planned":
                raise DomainError(
                    "cannot edit contributions on a skipped route position"
                )

            if target_id:
                cursor.execute(
                    """
                    SELECT role
                    FROM round_participants
                    WHERE id = %s AND round_id = %s
                    """,
                    (target_id, round_uuid),
                )
                target = cursor.fetchone()
                if not target or target["role"] != "player":
                    raise DomainError(
                        "contribution target must be a player in this round"
                    )

            cursor.execute(
                """
                SELECT player_participant_id
                FROM scramble_contributions
                WHERE round_id = %s
                  AND route_position = %s
                  AND shot_type = %s
                FOR UPDATE
                """,
                (
                    round_uuid,
                    route_position,
                    normalized_type,
                ),
            )
            previous = cursor.fetchone()
            old_target = (
                previous["player_participant_id"]
                if previous
                else None
            )
            if old_target == target_id:
                return {
                    "round_id": round_uuid,
                    "route_position": route_position,
                    "hole": hole_number,
                    "shot_type": normalized_type,
                    "player_participant_id": target_id,
                }

            if target_id is None:
                cursor.execute(
                    """
                    DELETE FROM scramble_contributions
                    WHERE round_id = %s
                      AND route_position = %s
                      AND shot_type = %s
                    """,
                    (
                        round_uuid,
                        route_position,
                        normalized_type,
                    ),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO scramble_contributions (
                        round_id, route_position, hole_number,
                        shot_type, player_participant_id
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (
                        round_id, route_position, shot_type
                    )
                    DO UPDATE SET
                        hole_number = EXCLUDED.hole_number,
                        player_participant_id =
                            EXCLUDED.player_participant_id,
                        updated_at = now()
                    """,
                    (
                        round_uuid,
                        route_position,
                        hole_number,
                        normalized_type,
                        target_id,
                    ),
                )

            content_event = scramble_contribution_content_event(
                old_target,
                target_id,
                normalized_type,
            )
            self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=actor["id"],
                event_type="scramble_contribution_change",
                hole_number=hole_number,
                route_position=route_position,
                old_value=(
                    str(old_target)
                    if old_target
                    else None
                ),
                new_value=(
                    str(target_id)
                    if target_id
                    else None
                ),
                data={
                    "shot_type": normalized_type,
                    "player_participant_id": (
                        str(target_id)
                        if target_id
                        else None
                    ),
                },
                content_event_key=content_event,
                presentation_context={
                    "hole": hole_number,
                    "mode": round_row["mode"],
                },
            )
            return {
                "round_id": round_uuid,
                "route_position": route_position,
                "hole": hole_number,
                "shot_type": normalized_type,
                "player_participant_id": target_id,
            }

    @staticmethod
    def _response_target_event(
        cursor: Any,
        *,
        round_id: UUID,
        event_id: UUID,
        score_only: bool = False,
    ) -> dict[str, Any]:
        event_types = (
            "AND event_type IN ('score_report', 'score_push')"
            if score_only
            else ""
        )
        cursor.execute(
            f"""
            SELECT id, actor_participant_id, event_type, hole_number,
                   route_position, data
            FROM round_events
            WHERE id = %s AND round_id = %s
              {event_types}
            """,
            (event_id, round_id),
        )
        event = cursor.fetchone()
        if not event:
            label = "score event" if score_only else "event"
            raise DomainError(f"response target must be an {label} in this round")
        return event

    def set_event_reaction(
        self,
        golfer_id: object,
        round_id: object,
        event_id: object,
        reaction_kind: object,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        event_uuid = self._uuid(event_id, "event_id")
        kind = str(reaction_kind or "").strip().lower()
        allowed = {"bullshit", "cheater", "lucky", "nice", "talk_shit"}
        if kind not in allowed:
            raise DomainError("unsupported reaction")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid)
            actor = self._participant(cursor, round_uuid, golfer_uuid)
            if round_row["status"] not in {"active", "completed"}:
                raise DomainError("reactions are only available on active or completed rounds")
            self._response_target_event(
                cursor,
                round_id=round_uuid,
                event_id=event_uuid,
            )

            cursor.execute(
                """
                INSERT INTO round_event_reactions (
                    event_id, actor_participant_id, reaction_kind
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (event_id, actor_participant_id)
                DO UPDATE SET reaction_kind = EXCLUDED.reaction_kind,
                              updated_at = now()
                RETURNING event_id, actor_participant_id,
                          reaction_kind, created_at, updated_at
                """,
                (event_uuid, actor["id"], kind),
            )
            return cursor.fetchone()

    def remove_event_reaction(
        self,
        golfer_id: object,
        round_id: object,
        event_id: object,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        event_uuid = self._uuid(event_id, "event_id")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid)
            actor = self._participant(cursor, round_uuid, golfer_uuid)
            if round_row["status"] not in {"active", "completed"}:
                raise DomainError("reactions are only available on active or completed rounds")
            self._response_target_event(
                cursor,
                round_id=round_uuid,
                event_id=event_uuid,
            )
            cursor.execute(
                """
                DELETE FROM round_event_reactions
                WHERE event_id = %s AND actor_participant_id = %s
                RETURNING reaction_kind
                """,
                (event_uuid, actor["id"]),
            )
            removed = cursor.fetchone()
            return {
                "event_id": event_uuid,
                "actor_participant_id": actor["id"],
                "removed": bool(removed),
            }

    def set_score_challenge(
        self,
        golfer_id: object,
        round_id: object,
        score_event_id: object,
        *,
        proposed_score: object | None = None,
        comment: object | None = None,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        score_event_uuid = self._uuid(score_event_id, "score_event_id")

        proposed: int | None = None
        if proposed_score not in (None, ""):
            try:
                proposed = int(proposed_score)
            except (TypeError, ValueError) as error:
                raise DomainError("proposed score must be between 1 and 99") from error
            if not 1 <= proposed <= 99:
                raise DomainError("proposed score must be between 1 and 99")

        challenge_comment = str(comment or "").strip()
        if len(challenge_comment) > 280:
            raise DomainError("challenge comment must be 280 characters or fewer")
        if proposed is None and not challenge_comment:
            raise DomainError("challenge needs a proposed score or comment")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid)
            challenger = self._participant(cursor, round_uuid, golfer_uuid)
            if round_row["status"] not in {"active", "completed"}:
                raise DomainError("score challenges are only available on active or completed rounds")

            score_event = self._response_target_event(
                cursor,
                round_id=round_uuid,
                event_id=score_event_uuid,
                score_only=True,
            )
            if score_event["actor_participant_id"] == challenger["id"]:
                raise DomainError("you cannot challenge a score you entered yourself")

            cursor.execute(
                """
                SELECT status
                FROM score_challenges
                WHERE score_event_id = %s
                  AND challenger_participant_id = %s
                """,
                (score_event_uuid, challenger["id"]),
            )
            previous = cursor.fetchone()
            action = "updated" if previous and previous["status"] == "active" else "filed"

            cursor.execute(
                """
                INSERT INTO score_challenges (
                    score_event_id, challenger_participant_id,
                    proposed_score, comment, status
                )
                VALUES (%s, %s, %s, %s, 'active')
                ON CONFLICT (score_event_id, challenger_participant_id)
                DO UPDATE SET proposed_score = EXCLUDED.proposed_score,
                              comment = EXCLUDED.comment,
                              status = 'active',
                              updated_at = now()
                RETURNING score_event_id, challenger_participant_id,
                          proposed_score, comment, status,
                          created_at, updated_at
                """,
                (
                    score_event_uuid,
                    challenger["id"],
                    proposed,
                    challenge_comment or None,
                ),
            )
            challenge = cursor.fetchone()

            self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=challenger["id"],
                event_type="score_challenge",
                hole_number=score_event["hole_number"],
                route_position=score_event["route_position"],
                data={
                    "score_event_id": str(score_event_uuid),
                    "proposed_score": proposed,
                    "message": challenge_comment or None,
                    "action": action,
                },
                reply_to_event_id=score_event_uuid,
                content_event_key="score.challenge",
                presentation_context={
                    "hole": score_event["hole_number"] or "",
                    "mode": round_row["mode"],
                },
            )
            return challenge

    def withdraw_score_challenge(
        self,
        golfer_id: object,
        round_id: object,
        score_event_id: object,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        score_event_uuid = self._uuid(score_event_id, "score_event_id")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid)
            challenger = self._participant(cursor, round_uuid, golfer_uuid)
            if round_row["status"] not in {"active", "completed"}:
                raise DomainError("score challenges are only available on active or completed rounds")

            score_event = self._response_target_event(
                cursor,
                round_id=round_uuid,
                event_id=score_event_uuid,
                score_only=True,
            )
            cursor.execute(
                """
                UPDATE score_challenges
                SET status = 'withdrawn', updated_at = now()
                WHERE score_event_id = %s
                  AND challenger_participant_id = %s
                  AND status = 'active'
                RETURNING score_event_id, challenger_participant_id,
                          proposed_score, comment, status,
                          created_at, updated_at
                """,
                (score_event_uuid, challenger["id"]),
            )
            challenge = cursor.fetchone()
            if not challenge:
                raise DomainError("you do not have an active challenge on this score")

            self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=challenger["id"],
                event_type="score_challenge_withdrawn",
                hole_number=score_event["hole_number"],
                route_position=score_event["route_position"],
                data={
                    "score_event_id": str(score_event_uuid),
                    "action": "withdrawn",
                },
                reply_to_event_id=score_event_uuid,
                content_event_key="score.challenge.withdrawn",
                presentation_context={
                    "hole": score_event["hole_number"] or "",
                    "mode": round_row["mode"],
                },
            )
            return challenge

    def add_score_response(
        self,
        golfer_id: object,
        round_id: object,
        score_event_id: object,
        *,
        response_kind: object,
        message: object | None = None,
        target_participant_id: object | None = None,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        parent_event_uuid = self._uuid(score_event_id, "score_event_id")
        kind = str(response_kind or "").strip().lower()
        allowed = {"blame", "custom"}
        if kind not in allowed:
            raise DomainError(
                "quick reactions must use the event reaction endpoint"
            )

        response_message = str(message or "").strip()
        if len(response_message) > 280:
            raise DomainError("score response must be 280 characters or fewer")
        if kind == "custom" and not response_message:
            raise DomainError("custom score response cannot be empty")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid)
            actor = self._participant(cursor, round_uuid, golfer_uuid)
            if round_row["status"] not in {"active", "completed"}:
                raise DomainError(
                    "score responses are only available on active or completed rounds"
                )

            cursor.execute(
                """
                SELECT id, event_type, hole_number, route_position, data
                FROM round_events
                WHERE id = %s
                  AND round_id = %s
                  AND event_type IN ('score_report', 'score_push')
                """,
                (parent_event_uuid, round_uuid),
            )
            score_event = cursor.fetchone()
            if not score_event:
                raise DomainError("response target must be a score event in this round")

            score_data = score_event.get("data") or {}
            target_id: UUID | None = None

            if round_row["mode"] == "individual":
                subject_value = score_data.get("player_participant_id")
                if subject_value:
                    target_id = self._uuid(
                        subject_value,
                        "player_participant_id",
                    )
            elif target_participant_id is not None:
                target_id = self._uuid(
                    target_participant_id,
                    "target_participant_id",
                )

            if kind == "blame" and round_row["mode"] == "scramble" and target_id is None:
                raise DomainError("pick who screwed up before blaming someone")

            if target_id is not None:
                cursor.execute(
                    """
                    SELECT role
                    FROM round_participants
                    WHERE id = %s AND round_id = %s
                    """,
                    (target_id, round_uuid),
                )
                target = cursor.fetchone()
                if not target or target["role"] != "player":
                    raise DomainError("score response target must be a player in this round")

            payload: dict[str, object] = {
                "response_kind": kind,
                "score_event_id": str(parent_event_uuid),
            }
            if target_id is not None:
                payload["target_participant_id"] = str(target_id)
            if response_message:
                payload["message"] = response_message

            content_event = (
                None
                if kind == "custom"
                else score_response_content_event(kind)
            )
            return self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=actor["id"],
                event_type="score_response",
                hole_number=score_event["hole_number"],
                route_position=score_event["route_position"],
                data=payload,
                reply_to_event_id=parent_event_uuid,
                content_event_key=content_event,
                presentation_context={
                    "hole": score_event["hole_number"] or "",
                    "mode": round_row["mode"],
                },
            )

    def add_social_event(
        self,
        golfer_id: object,
        round_id: object,
        event_type: object,
        *,
        hole: object | None = None,
        data: object | None = None,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        kind = str(event_type or "")
        payload = data if isinstance(data, dict) else {}
        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid)
            participant = self._participant(cursor, round_uuid, golfer_uuid)
            validate_social_event(participant["role"], kind)

            if round_row["status"] != "active":
                raise DomainError("Bag of Bullshit is only available during an active round")

            route_position = (
                int(hole)
                if hole is not None
                else int(round_row["current_route_position"])
            )
            route_row = self._route_position(
                cursor,
                round_uuid,
                route_position,
            )
            if route_position > int(round_row["current_route_position"]):
                raise DomainError(
                    "future holes are preview-only until they become active"
                )
            hole_number = int(route_row["hole_number"])

            target_value = payload.get("target_participant_id")
            if target_value is not None:
                target_id = self._uuid(
                    target_value,
                    "target_participant_id",
                )
                cursor.execute(
                    """
                    SELECT 1
                    FROM round_participants
                    WHERE id = %s AND round_id = %s
                    """,
                    (target_id, round_uuid),
                )
                if not cursor.fetchone():
                    raise DomainError(
                        "target must be a participant in this round"
                    )
                payload["target_participant_id"] = str(target_id)

            if kind == "open_mic":
                message = str(payload.get("message", "")).strip()
                if not 1 <= len(message) <= 280:
                    raise DomainError(
                        "Open Mic message must be between 1 and 280 characters"
                    )
                payload = {"message": message}
            elif kind == "reaction":
                reaction = str(payload.get("reaction", "")).strip().lower()
                if reaction not in {"laugh", "bullshit", "applause"}:
                    raise DomainError("unsupported reaction")
                payload = {"reaction": reaction}
            else:
                message = str(payload.get("message", "")).strip()
                if message:
                    if len(message) > 280:
                        raise DomainError(
                            "Bag of Bullshit message must be 280 characters or fewer"
                        )
                    payload["message"] = message
                else:
                    payload.pop("message", None)

            content_event = social_content_event(kind, payload)
            return self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=participant["id"],
                event_type=kind,
                hole_number=hole_number,
                route_position=route_position,
                data=payload,
                content_event_key=content_event,
                presentation_context={
                    "hole": hole_number if hole_number is not None else "",
                    "mode": round_row["mode"],
                },
            )

    def search_cached_courses(
        self,
        query: object,
        *,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        search = str(query or "").strip()
        if len(search) < 2:
            raise DomainError("course search must be at least 2 characters")
        size = max(1, min(int(limit), 25))

        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, provider, external_course_id, name, cached_at
                FROM cached_courses
                WHERE name ILIKE %s
                ORDER BY
                    CASE WHEN lower(name) = lower(%s) THEN 0 ELSE 1 END,
                    name
                LIMIT %s
                """,
                (f"%{search}%", search, size),
            )
            return cursor.fetchall()

    def get_cached_course_by_external_id(
        self,
        external_course_id: object,
    ) -> dict[str, Any] | None:
        external_id = str(external_course_id or "").strip()
        if not external_id:
            raise DomainError("external_course_id is required")

        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, provider, external_course_id, name, cached_at
                FROM cached_courses
                WHERE provider = 'opengolfapi' AND external_course_id = %s
                """,
                (external_id,),
            )
            course = cursor.fetchone()
            if not course:
                return None
            course["tees"] = self._course_tees(
                cursor,
                course["id"],
                hole_count=18,
            )
            return course

    @staticmethod
    def _course_tees(
        cursor: Any,
        course_id: UUID,
        *,
        hole_count: int,
    ) -> list[dict[str, Any]]:
        cursor.execute(
            """
            SELECT tee_name,
                   count(*) AS holes_with_tee,
                   sum(yardage) FILTER (WHERE yardage IS NOT NULL) AS total_yardage
            FROM cached_course_hole_tees
            WHERE course_id = %s AND hole_number <= %s
            GROUP BY tee_name
            ORDER BY max(yardage) DESC NULLS LAST, tee_name
            """,
            (course_id, hole_count),
        )
        return cursor.fetchall()

    def get_cached_course(self, course_id: object) -> dict[str, Any]:
        course_uuid = self._uuid(course_id, "course_id")
        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, provider, external_course_id, name, cached_at
                FROM cached_courses
                WHERE id = %s
                """,
                (course_uuid,),
            )
            course = cursor.fetchone()
            if not course:
                raise NotFound("cached course not found")
            course["tees"] = self._course_tees(
                cursor,
                course_uuid,
                hole_count=18,
            )
            return course

    def set_participant_tee(
        self,
        golfer_id: object,
        round_id: object,
        tee_name: object,
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        selected_tee = self._clean_tee_name(tee_name)
        if not selected_tee:
            raise DomainError("tee_name is required")

        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            participant = self._participant(cursor, round_uuid, golfer_uuid)
            self._require_active_player(participant, "choose a tee")

            if round_row["status"] not in {"setup", "active"}:
                raise DomainError(
                    "tee can only be changed before or during an active round"
                )
            if round_row["course_id"]:
                self._validate_course_tee(
                    cursor,
                    round_row["course_id"],
                    selected_tee,
                )

            if round_row["mode"] == "scramble":
                old_tee = round_row.get("scramble_tee_name")
                cursor.execute(
                    """
                    UPDATE rounds
                    SET scramble_tee_name = %s, updated_at = now()
                    WHERE id = %s
                    RETURNING id AS round_id, scramble_tee_name
                    """,
                    (selected_tee, round_uuid),
                )
                updated = cursor.fetchone()
                updated["role"] = "team"
                updated["tee_name"] = updated["scramble_tee_name"]
                updated.pop("scramble_tee_name", None)
                scope = "team"
                subject_id = None
            else:
                old_tee = participant.get("tee_name")
                cursor.execute(
                    """
                    UPDATE round_participants
                    SET tee_name = %s
                    WHERE id = %s
                    RETURNING id, round_id, golfer_id, role, tee_name
                    """,
                    (selected_tee, participant["id"]),
                )
                updated = cursor.fetchone()
                scope = "player"
                subject_id = str(participant["id"])

            if old_tee != selected_tee:
                self._event(
                    cursor,
                    round_id=round_uuid,
                    actor_participant_id=participant["id"],
                    event_type="tee_change",
                    old_value=old_tee,
                    new_value=selected_tee,
                    data={
                        "scope": scope,
                        "player_participant_id": subject_id,
                    },
                    presentation_context={"mode": round_row["mode"]},
                )
            return updated

    def cache_course(self, snapshot: CourseSnapshot) -> UUID:
        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO cached_courses (provider, external_course_id, name)
                VALUES ('opengolfapi', %s, %s)
                ON CONFLICT (provider, external_course_id)
                DO UPDATE SET name = EXCLUDED.name, cached_at = now()
                RETURNING id
                """,
                (snapshot.external_id, snapshot.name),
            )
            course_id = cursor.fetchone()["id"]
            cursor.execute("DELETE FROM cached_course_holes WHERE course_id = %s", (course_id,))
            for hole in snapshot.holes:
                cursor.execute(
                    """
                    INSERT INTO cached_course_holes (course_id, hole_number, par, stroke_index)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (course_id, hole.number, hole.par, hole.stroke_index),
                )
                for tee_name, yardage in hole.tee_yardages.items():
                    cursor.execute(
                        """
                        INSERT INTO cached_course_hole_tees (
                            course_id, hole_number, tee_name, yardage
                        ) VALUES (%s, %s, %s, %s)
                        """,
                        (course_id, hole.number, tee_name, yardage),
                    )
            return course_id
