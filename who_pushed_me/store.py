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
from who_pushed_me.content.preferences import merge_preference_patch, public_preferences
from who_pushed_me.content.presentation import (
    build_shared_presentation,
    filter_presentation_for_preferences,
    par_content_event,
    score_content_event,
    scramble_contribution_content_event,
    social_content_event,
    status_content_event,
)
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
    require_player,
    validate_hole,
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
    def _participant(cursor: Any, round_id: UUID, golfer_id: UUID) -> dict[str, Any]:
        cursor.execute(
            """
            SELECT id, round_id, golfer_id, role
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
    def _round(cursor: Any, round_id: UUID, *, lock: bool = False) -> dict[str, Any]:
        cursor.execute(
            f"""
            SELECT id, mode, hole_count, active_code, current_hole, status,
                   course_id, free_play_name, created_at, updated_at
            FROM rounds WHERE id = %s{' FOR UPDATE' if lock else ''}
            """,
            (round_id,),
        )
        round_row = cursor.fetchone()
        if not round_row:
            raise NotFound("round not found")
        return round_row

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
        old_value: object | None = None,
        new_value: object | None = None,
        data: dict[str, object] | None = None,
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

        cursor.execute(
            """
            INSERT INTO round_events (
                round_id, actor_participant_id, event_type, hole_number,
                old_value, new_value, data, content_event_key, presentation
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, event_type, hole_number, old_value, new_value, data,
                      content_event_key, presentation, created_at
            """,
            (
                round_id,
                actor_participant_id,
                event_type,
                hole_number,
                Jsonb(old_value) if old_value is not None else None,
                Jsonb(new_value) if new_value is not None else None,
                Jsonb(data or {}),
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
    ) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_mode = str(mode or "")
        if round_mode not in ROUND_MODES:
            raise DomainError("mode must be individual or scramble")
        try:
            hole_count = int(holes)
        except (TypeError, ValueError) as error:
            raise DomainError("holes must be 9 or 18") from error
        if hole_count not in {9, 18}:
            raise DomainError("holes must be 9 or 18")
        cached_course_id = self._uuid(course_id, "course_id") if course_id else None
        free_play = str(free_play_name).strip() if free_play_name else None

        for _ in range(12):
            try:
                with self._connection() as connection, connection.cursor() as cursor:
                    code = generate_round_code()
                    cursor.execute(
                        """
                        INSERT INTO rounds (
                            mode, hole_count, active_code, course_id, free_play_name
                        ) VALUES (%s, %s, %s, %s, %s)
                        RETURNING id, mode, hole_count, active_code, current_hole, status,
                                  course_id, free_play_name, created_at
                        """,
                        (round_mode, hole_count, code, cached_course_id, free_play),
                    )
                    round_row = cursor.fetchone()
                    cursor.execute(
                        """
                        INSERT INTO round_participants (round_id, golfer_id, role)
                        VALUES (%s, %s, 'player')
                        RETURNING id
                        """,
                        (round_row["id"], golfer_uuid),
                    )
                    participant = cursor.fetchone()
                    self._event(
                        cursor,
                        round_id=round_row["id"],
                        actor_participant_id=participant["id"],
                        event_type="lobby_created",
                        data={"role": "player"},
                        content_event_key="lobby.created",
                        presentation_context={"mode": round_mode},
                    )
                    if cached_course_id:
                        cursor.execute(
                            """
                            INSERT INTO round_hole_pars (round_id, hole_number, par)
                            SELECT %s, hole_number, par
                            FROM cached_course_holes
                            WHERE course_id = %s AND hole_number <= %s AND par IS NOT NULL
                            """,
                            (round_row["id"], cached_course_id, hole_count),
                        )
                    round_row["participant_id"] = participant["id"]
                    round_row["role"] = "player"
                    return round_row
            except errors.UniqueViolation as error:
                if error.diag.constraint_name != "rounds_live_code_unique":
                    raise
        raise RuntimeError("could not allocate a unique active round code")

    def join_round(self, golfer_id: object, *, code: object, role: object) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_code = str(code or "").strip()
        participant_role = str(role or "")
        if len(round_code) != 4 or not round_code.isdigit():
            raise DomainError("round code must be four digits")
        if participant_role not in PARTICIPANT_ROLES:
            raise DomainError("role must be player or spectator")
        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, mode FROM rounds
                WHERE active_code = %s AND status IN ('setup', 'active')
                """,
                (round_code,),
            )
            round_row = cursor.fetchone()
            if not round_row:
                raise NotFound("active round not found")

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

            cursor.execute(
                """
                INSERT INTO round_participants (round_id, golfer_id, role)
                VALUES (%s, %s, %s)
                ON CONFLICT (round_id, golfer_id) DO NOTHING
                RETURNING id, round_id, golfer_id, role, joined_at
                """,
                (round_row["id"], golfer_uuid, participant_role),
            )
            participant = cursor.fetchone()
            if participant:
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
                    data={"role": participant_role},
                    content_event_key=content_event,
                    presentation_context={"mode": round_row["mode"]},
                )
                return participant

            cursor.execute(
                """
                SELECT id, round_id, golfer_id, role, joined_at
                FROM round_participants WHERE round_id = %s AND golfer_id = %s
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
                data={"role": participant["role"]},
                content_event_key=reconnect_event,
                presentation_context={"mode": round_row["mode"]},
            )
            return participant

    def get_round(self, golfer_id: object, code: object) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_code = str(code or "").strip()
        with self._connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT id FROM rounds WHERE active_code = %s", (round_code,))
            found = cursor.fetchone()
            if not found:
                raise NotFound("round not found")
            round_row = self._round(cursor, found["id"])
            participant = self._participant(cursor, found["id"], golfer_uuid)
            cursor.execute(
                """
                SELECT rp.id, rp.role, rp.joined_at, g.id AS golfer_id, g.display_name
                FROM round_participants rp JOIN golfers g ON g.id = rp.golfer_id
                WHERE rp.round_id = %s ORDER BY rp.joined_at, rp.id
                """,
                (found["id"],),
            )
            round_row["participants"] = cursor.fetchall()
            cursor.execute(
                """
                SELECT hole_number, par FROM round_hole_pars
                WHERE round_id = %s ORDER BY hole_number
                """,
                (found["id"],),
            )
            round_row["pars"] = cursor.fetchall()
            cursor.execute(
                """
                SELECT id, hole_number, score_scope, player_participant_id, strokes, updated_at
                FROM round_hole_scores WHERE round_id = %s
                ORDER BY hole_number, player_participant_id NULLS FIRST
                """,
                (found["id"],),
            )
            round_row["scores"] = cursor.fetchall()
            cursor.execute(
                """
                SELECT hole_number, shot_type, player_participant_id, updated_at
                FROM scramble_contributions WHERE round_id = %s
                ORDER BY hole_number, shot_type
                """,
                (found["id"],),
            )
            round_row["contributions"] = cursor.fetchall()
            cursor.execute(
                """
                SELECT id, actor_participant_id, event_type, hole_number,
                       old_value, new_value, data, content_event_key,
                       presentation, created_at
                FROM round_events WHERE round_id = %s
                ORDER BY created_at DESC, id DESC LIMIT 100
                """,
                (found["id"],),
            )
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
            round_row["viewer_role"] = participant["role"]
            return round_row

    def set_current_hole(self, golfer_id: object, round_id: object, hole: object) -> dict[str, Any]:
        golfer_uuid = self._uuid(golfer_id, "golfer_id")
        round_uuid = self._uuid(round_id, "round_id")
        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid, lock=True)
            participant = self._participant(cursor, round_uuid, golfer_uuid)
            require_player(participant["role"], "change the current hole")
            hole_number = validate_hole(hole, round_row["hole_count"])
            old_hole = round_row["current_hole"]
            if old_hole != hole_number:
                cursor.execute(
                    "UPDATE rounds SET current_hole = %s, updated_at = now() WHERE id = %s",
                    (hole_number, round_uuid),
                )
                self._event(
                    cursor,
                    round_id=round_uuid,
                    actor_participant_id=participant["id"],
                    event_type="current_hole_change",
                    old_value=old_hole,
                    new_value=hole_number,
                    content_event_key=(
                        "hole.advance"
                        if hole_number == old_hole + 1
                        else "hole.enter"
                    ),
                    presentation_context={
                        "hole": hole_number,
                        "mode": round_row["mode"],
                    },
                )
            return {"round_id": round_uuid, "current_hole": hole_number}

    def set_status(self, golfer_id: object, round_id: object, status: object) -> dict[str, Any]:
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
            require_player(participant["role"], "change round status")
            old_status = round_row["status"]
            if new_status != old_status:
                if new_status not in transitions[old_status]:
                    raise DomainError(f"cannot change round from {old_status} to {new_status}")
                cursor.execute(
                    "UPDATE rounds SET status = %s, updated_at = now() WHERE id = %s",
                    (new_status, round_uuid),
                )
                content_event = status_content_event(old_status, new_status)
                self._event(
                    cursor,
                    round_id=round_uuid,
                    actor_participant_id=participant["id"],
                    event_type="round_status_change",
                    old_value=old_status,
                    new_value=new_status,
                    content_event_key=content_event,
                    presentation_context={"mode": round_row["mode"]},
                )
            return {"round_id": round_uuid, "status": new_status}

    def set_par(self, golfer_id: object, round_id: object, hole: object, par: object) -> dict[str, Any]:
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
            participant = self._participant(cursor, round_uuid, golfer_uuid)
            require_player(participant["role"], "change par")
            hole_number = validate_hole(hole, round_row["hole_count"])
            cursor.execute(
                "SELECT par FROM round_hole_pars WHERE round_id = %s AND hole_number = %s FOR UPDATE",
                (round_uuid, hole_number),
            )
            previous = cursor.fetchone()
            old_par = previous["par"] if previous else None
            if old_par == par_value:
                return {"round_id": round_uuid, "hole": hole_number, "par": par_value, "event": None}
            cursor.execute(
                """
                INSERT INTO round_hole_pars (round_id, hole_number, par)
                VALUES (%s, %s, %s)
                ON CONFLICT (round_id, hole_number)
                DO UPDATE SET par = EXCLUDED.par, updated_at = now()
                """,
                (round_uuid, hole_number, par_value),
            )
            event = self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=participant["id"],
                event_type=audit_event_type("par", old_par),
                hole_number=hole_number,
                old_value=old_par,
                new_value=par_value,
                content_event_key=par_content_event(old_par, par_value),
                presentation_context={
                    "hole": hole_number,
                    "par": par_value,
                    "mode": round_row["mode"],
                },
            )
            return {"round_id": round_uuid, "hole": hole_number, "par": par_value, "event": event}

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
            round_row = self._round(cursor, round_uuid)
            actor = self._participant(cursor, round_uuid, golfer_uuid)
            require_player(actor["role"], "change scores")
            hole_number = validate_hole(hole, round_row["hole_count"])
            if round_row["mode"] == "individual":
                target_id = self._uuid(player_participant_id, "player_participant_id")
                cursor.execute(
                    "SELECT role FROM round_participants WHERE id = %s AND round_id = %s",
                    (target_id, round_uuid),
                )
                target = cursor.fetchone()
                if not target or target["role"] != "player":
                    raise DomainError("score target must be a player in this round")
                scope = "player"
            else:
                if player_participant_id is not None:
                    raise DomainError("scramble rounds use one team score")
                target_id = None
                scope = "team"
            cursor.execute(
                """
                SELECT id, strokes FROM round_hole_scores
                WHERE round_id = %s AND hole_number = %s
                  AND score_scope = %s
                  AND player_participant_id IS NOT DISTINCT FROM %s
                FOR UPDATE
                """,
                (round_uuid, hole_number, scope, target_id),
            )
            previous = cursor.fetchone()
            old_score = previous["strokes"] if previous else None
            if old_score == stroke_value:
                return {"round_id": round_uuid, "hole": hole_number, "strokes": stroke_value, "event": None}
            if previous:
                cursor.execute(
                    "UPDATE round_hole_scores SET strokes = %s, updated_at = now() WHERE id = %s",
                    (stroke_value, previous["id"]),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO round_hole_scores (
                        round_id, hole_number, score_scope, player_participant_id, strokes
                    ) VALUES (%s, %s, %s, %s, %s)
                    """,
                    (round_uuid, hole_number, scope, target_id, stroke_value),
                )
            cursor.execute(
                """
                SELECT par
                FROM round_hole_pars
                WHERE round_id = %s AND hole_number = %s
                """,
                (round_uuid, hole_number),
            )
            par_row = cursor.fetchone()
            par_value = par_row["par"] if par_row else None
            content_event = score_content_event(
                mode=round_row["mode"],
                old_score=old_score,
                new_score=stroke_value,
                par=par_value,
                hole_number=hole_number,
                current_hole=round_row["current_hole"],
            )
            event = self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=actor["id"],
                event_type=audit_event_type("score", old_score),
                hole_number=hole_number,
                old_value=old_score,
                new_value=stroke_value,
                data={
                    "scope": scope,
                    "player_participant_id": str(target_id) if target_id else None,
                },
                content_event_key=content_event,
                presentation_context={
                    "hole": hole_number,
                    "par": par_value if par_value is not None else "",
                    "strokes": stroke_value,
                    "old_score": old_score if old_score is not None else "",
                    "new_score": stroke_value,
                    "mode": round_row["mode"],
                    "score_name": content_event.rsplit(".", 1)[-1],
                },
            )
            return {"round_id": round_uuid, "hole": hole_number, "strokes": stroke_value, "event": event}

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
            self._uuid(player_participant_id, "player_participant_id")
            if player_participant_id is not None
            else None
        )
        with self._connection() as connection, connection.cursor() as cursor:
            round_row = self._round(cursor, round_uuid)
            actor = self._participant(cursor, round_uuid, golfer_uuid)
            require_player(actor["role"], "change scramble contributions")
            if round_row["mode"] != "scramble":
                raise DomainError("contributions are only available for scramble rounds")
            hole_number = validate_hole(hole, round_row["hole_count"])
            if target_id:
                cursor.execute(
                    "SELECT role FROM round_participants WHERE id = %s AND round_id = %s",
                    (target_id, round_uuid),
                )
                target = cursor.fetchone()
                if not target or target["role"] != "player":
                    raise DomainError("contribution target must be a player in this round")
            cursor.execute(
                """
                SELECT player_participant_id FROM scramble_contributions
                WHERE round_id = %s AND hole_number = %s AND shot_type = %s
                FOR UPDATE
                """,
                (round_uuid, hole_number, normalized_type),
            )
            previous = cursor.fetchone()
            old_target = previous["player_participant_id"] if previous else None
            if old_target == target_id:
                return {"round_id": round_uuid, "hole": hole_number, "shot_type": normalized_type}
            if target_id is None:
                cursor.execute(
                    """
                    DELETE FROM scramble_contributions
                    WHERE round_id = %s AND hole_number = %s AND shot_type = %s
                    """,
                    (round_uuid, hole_number, normalized_type),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO scramble_contributions (
                        round_id, hole_number, shot_type, player_participant_id
                    ) VALUES (%s, %s, %s, %s)
                    ON CONFLICT (round_id, hole_number, shot_type)
                    DO UPDATE SET player_participant_id = EXCLUDED.player_participant_id,
                                  updated_at = now()
                    """,
                    (round_uuid, hole_number, normalized_type, target_id),
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
                old_value=str(old_target) if old_target else None,
                new_value=str(target_id) if target_id else None,
                data={
                    "shot_type": normalized_type,
                    "player_participant_id": str(target_id) if target_id else None,
                },
                content_event_key=content_event,
                presentation_context={
                    "hole": hole_number,
                    "mode": round_row["mode"],
                },
            )
            return {
                "round_id": round_uuid,
                "hole": hole_number,
                "shot_type": normalized_type,
                "player_participant_id": target_id,
            }

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
            hole_number = validate_hole(hole, round_row["hole_count"]) if hole is not None else None
            if kind == "open_mic":
                message = str(payload.get("message", "")).strip()
                if not 1 <= len(message) <= 280:
                    raise DomainError("Open Mic message must be between 1 and 280 characters")
                payload = {"message": message}
            elif kind == "reaction":
                reaction = str(payload.get("reaction", "")).strip()
                if not 1 <= len(reaction) <= 32:
                    raise DomainError("reaction must be between 1 and 32 characters")
                payload = {"reaction": reaction}
            content_event = social_content_event(kind, payload)
            return self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=participant["id"],
                event_type=kind,
                hole_number=hole_number,
                data=payload,
                content_event_key=content_event,
                presentation_context={
                    "hole": hole_number if hole_number is not None else "",
                    "mode": round_row["mode"],
                },
            )

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
