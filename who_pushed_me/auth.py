from __future__ import annotations

import hashlib
import re
import secrets
from datetime import timedelta
from typing import Final

from werkzeug.security import check_password_hash, generate_password_hash

from who_pushed_me.domain import DomainError

USERNAME_RE: Final = re.compile(r"^[a-z0-9][a-z0-9_.-]{2,15}$")
LEGACY_USERNAME_RE: Final = re.compile(r"^[a-z0-9][a-z0-9_.-]{2,23}$")
RECOVERY_ALPHABET: Final = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
RECOVERY_KEY_RE: Final = re.compile(r"^[A-HJ-KM-NP-Z2-9]{4}-[A-HJ-KM-NP-Z2-9]{4}$")
LEGACY_RECOVERY_KEY_RE: Final = re.compile(
    r"^[A-HJ-KM-NP-Z2-9]{4}(?:-[A-HJ-KM-NP-Z2-9]{4}){3}$"
)
SESSION_TTL: Final = timedelta(days=30)

_OBVIOUS_PASSWORDS: Final = frozenset(
    {
        "password",
        "password1",
        "password12",
        "password123",
        "password1234",
        "letmein123",
        "qwerty1234",
        "welcome123",
        "iloveyou",
        "football",
        "baseball",
        "basketball",
        "sunshine",
        "princess",
        "superman",
        "whatever",
        "computer",
        "internet",
        "golfgolfgolf",
    }
)
_SEQUENCE_SOURCES: Final = (
    "012345678901234567890123456789",
    "987654321098765432109876543210",
    "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz",
    "zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba",
    "qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnm",
)


def normalize_username(value: object) -> str:
    username = str(value or "").strip().lower()
    if not USERNAME_RE.fullmatch(username):
        raise DomainError(
            "username must be 3-16 characters using letters, numbers, ., _, or -"
        )
    return username


def normalize_login_username(value: object) -> str:
    """Allow pre-policy usernames to keep signing in while new names cap at 16."""
    username = str(value or "").strip().lower()
    if not LEGACY_USERNAME_RE.fullmatch(username):
        raise DomainError("invalid username")
    return username


def validate_password(value: object) -> str:
    password = str(value or "")
    if not 10 <= len(password) <= 128:
        raise DomainError("password must be between 10 and 128 characters")

    lowered = password.strip().lower()
    compact = re.sub(r"[^a-z0-9]+", "", lowered)

    if password.isdigit():
        raise DomainError("password cannot be all numbers")
    if lowered and len(set(lowered)) == 1:
        raise DomainError("password is too obvious")
    if lowered in _SEQUENCE_SOURCES or any(
        lowered and lowered in source for source in _SEQUENCE_SOURCES
    ):
        raise DomainError("password is too obvious")
    if lowered in _OBVIOUS_PASSWORDS or compact in _OBVIOUS_PASSWORDS:
        raise DomainError("password is too obvious")

    return password


def hash_password(password: object) -> str:
    return generate_password_hash(validate_password(password), method="scrypt")


def verify_password(password_hash: str, password: object) -> bool:
    # Login remains compatible with passwords created under the previous 8-char rule.
    candidate = str(password or "")
    if not 1 <= len(candidate) <= 128:
        return False
    return check_password_hash(password_hash, candidate)


def generate_recovery_key() -> str:
    raw = "".join(secrets.choice(RECOVERY_ALPHABET) for _ in range(8))
    return f"{raw[:4]}-{raw[4:]}"


def normalize_recovery_key(value: object) -> str:
    key = str(value or "").strip().upper()
    if not (
        RECOVERY_KEY_RE.fullmatch(key)
        or LEGACY_RECOVERY_KEY_RE.fullmatch(key)
    ):
        raise DomainError("recovery key must use the format XXXX-XXXX")
    return key


def hash_recovery_key(value: object) -> str:
    normalized = normalize_recovery_key(value)
    return hashlib.sha256(normalized.encode("ascii")).hexdigest()


def generate_session_token() -> str:
    return secrets.token_urlsafe(32)


def hash_session_token(token: object) -> str:
    value = str(token or "").strip()
    if len(value) < 32:
        raise DomainError("invalid session token")
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
