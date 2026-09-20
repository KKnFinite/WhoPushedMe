from __future__ import annotations

import re
import secrets
from typing import Final

RECOVERY_ALPHABET: Final = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
RECOVERY_KEY_RE: Final = re.compile(r"^[A-HJ-KM-NP-Z2-9]{3}-[A-HJ-KM-NP-Z2-9]{3}$")
ROUND_MODES: Final = frozenset({"individual", "scramble"})
ROUND_STATUSES: Final = frozenset({"setup", "active", "completed", "abandoned"})
PARTICIPANT_ROLES: Final = frozenset({"player", "spectator"})
SOCIAL_EVENT_TYPES: Final = frozenset(
    {"callout", "praise", "excuse", "open_mic", "reaction", "shot_call", "challenge"}
)
SPECTATOR_EVENT_TYPES: Final = frozenset({"open_mic", "reaction"})
SUGGESTED_SHOT_TYPES: Final = ("drive", "second", "approach", "recovery", "putt", "other")


class DomainError(ValueError):
    """Raised when a requested round operation violates domain rules."""


class PermissionDenied(DomainError):
    """Raised when a participant role cannot perform an operation."""


class NotFound(DomainError):
    """Raised when a requested record is not available."""


def clean_display_name(value: object) -> str:
    name = str(value or "").strip()
    if not 1 <= len(name) <= 40:
        raise DomainError("display_name must be between 1 and 40 characters")
    return name


def generate_recovery_key() -> str:
    raw = "".join(secrets.choice(RECOVERY_ALPHABET) for _ in range(6))
    return f"{raw[:3]}-{raw[3:]}"


def normalize_recovery_key(value: object) -> str:
    key = str(value or "").strip().upper()
    if not RECOVERY_KEY_RE.fullmatch(key):
        raise DomainError("recovery key must use the format XXX-XXX")
    return key


def generate_round_code() -> str:
    return f"{secrets.randbelow(9000) + 1000:04d}"


def require_player(role: str, operation: str = "change golf state") -> None:
    if role != "player":
        raise PermissionDenied(f"spectators cannot {operation}")


def validate_social_event(role: str, event_type: str) -> str:
    if event_type not in SOCIAL_EVENT_TYPES:
        raise DomainError("unsupported social event type")
    if role == "spectator" and event_type not in SPECTATOR_EVENT_TYPES:
        raise PermissionDenied("spectators may only add reactions and Open Mic messages")
    return event_type


def audit_event_type(subject: str, old_value: object | None) -> str:
    if subject not in {"score", "par"}:
        raise DomainError("unsupported audit subject")
    return f"{subject}_{'report' if old_value is None else 'push'}"


def require_active_round(status: str, operation: str = "change golf state") -> None:
    if status != "active":
        raise DomainError(f"round must be active to {operation}")


def validate_shared_hole_change(old_hole: int, new_hole: int) -> int:
    if new_hole < old_hole:
        raise DomainError("shared current hole cannot move backward")
    return new_hole


def validate_hole(hole: object, hole_count: int) -> int:
    try:
        value = int(hole)
    except (TypeError, ValueError) as error:
        raise DomainError("hole must be a number") from error
    if not 1 <= value <= hole_count:
        raise DomainError(f"hole must be between 1 and {hole_count}")
    return value


def normalize_shot_type(value: object) -> str:
    shot_type = re.sub(r"[^a-z0-9_-]+", "_", str(value or "").strip().lower()).strip("_")
    if not 1 <= len(shot_type) <= 32:
        raise DomainError("shot_type must be between 1 and 32 characters")
    return shot_type
