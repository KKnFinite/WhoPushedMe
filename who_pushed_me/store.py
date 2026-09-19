from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Iterator
from uuid import UUID

import psycopg
from psycopg import errors
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from who_pushed_me.courses import CourseSnapshot
from who_pushed_me.content.catalog import ContentCatalog, ContentError
from who_pushed_me.content.preferences import merge_preference_patch, public_preferences
from who_pushed_me.domain import (
    DomainError,
    NotFound,
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
    def _event(
        cursor: Any,
        *,
        round_id: UUID,
        actor_participant_id: UUID,
        event_type: str,
        hole_number: int | None = None,
        old_value: object | None = None,
        new_value: object | None = None,
        data: dict[str, object] | None = None,
    ) -> dict[str, Any]:
        cursor.execute(
            """
            INSERT INTO round_events (
                round_id, actor_participant_id, event_type, hole_number,
                old_value, new_value, data
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, event_type, hole_number, old_value, new_value, data, created_at
            """,
            (
                round_id,
                actor_participant_id,
                event_type,
                hole_number,
                Jsonb(old_value) if old_value is not None else None,
                Jsonb(new_value) if new_value is not None else None,
                Jsonb(data or {}),
            ),
        )
        return cursor.fetchone()

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
                except Exception:
                    continue
                overrides[key] = bool(row["enabled"])

            return {
                "mini_mascots_enabled": bool(settings["mini_mascots_enabled"]),
                "trash_talk_enabled": bool(settings["trash_talk_enabled"]),
                "event_overrides": overrides,
            }

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
                SELECT id FROM rounds
                WHERE active_code = %s AND status IN ('setup', 'active')
                """,
                (round_code,),
            )
            round_row = cursor.fetchone()
            if not round_row:
                raise NotFound("active round not found")
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
                return participant
            cursor.execute(
                """
                SELECT id, round_id, golfer_id, role, joined_at
                FROM round_participants WHERE round_id = %s AND golfer_id = %s
                """,
                (round_row["id"], golfer_uuid),
            )
            return cursor.fetchone()

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
                       old_value, new_value, data, created_at
                FROM round_events WHERE round_id = %s
                ORDER BY created_at DESC, id DESC LIMIT 100
                """,
                (found["id"],),
            )
            round_row["events"] = cursor.fetchall()
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
                self._event(
                    cursor,
                    round_id=round_uuid,
                    actor_participant_id=participant["id"],
                    event_type="round_status_change",
                    old_value=old_status,
                    new_value=new_status,
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
            event = self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=actor["id"],
                event_type=audit_event_type("score", old_score),
                hole_number=hole_number,
                old_value=old_score,
                new_value=stroke_value,
                data={"scope": scope, "player_participant_id": str(target_id) if target_id else None},
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
            self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=actor["id"],
                event_type="scramble_contribution_change",
                hole_number=hole_number,
                old_value=str(old_target) if old_target else None,
                new_value=str(target_id) if target_id else None,
                data={"shot_type": normalized_type},
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
            return self._event(
                cursor,
                round_id=round_uuid,
                actor_participant_id=participant["id"],
                event_type=kind,
                hole_number=hole_number,
                data=payload,
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
