from __future__ import annotations

import hashlib
import re
import secrets
from datetime import timedelta
from typing import Final

from werkzeug.security import check_password_hash, generate_password_hash

from who_pushed_me.domain import DomainError

USERNAME_RE: Final = re.compile(r"^[a-z0-9][a-z0-9_.-]{2,23}$")
RECOVERY_ALPHABET: Final = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
RECOVERY_KEY_RE: Final = re.compile(
    r"^[A-HJ-KM-NP-Z2-9]{4}(?:-[A-HJ-KM-NP-Z2-9]{4}){3}$"
)
SESSION_TTL: Final = timedelta(days=30)


def normalize_username(value: object) -> str:
    username = str(value or "").strip().lower()
    if not USERNAME_RE.fullmatch(username):
        raise DomainError(
            "username must be 3-24 characters using letters, numbers, ., _, or -"
        )
    return username


def validate_password(value: object) -> str:
    password = str(value or "")
    if not 8 <= len(password) <= 128:
        raise DomainError("password must be between 8 and 128 characters")
    return password


def hash_password(password: object) -> str:
    return generate_password_hash(validate_password(password), method="scrypt")


def verify_password(password_hash: str, password: object) -> bool:
    try:
        candidate = validate_password(password)
    except DomainError:
        return False
    return check_password_hash(password_hash, candidate)


def generate_recovery_key() -> str:
    raw = "".join(secrets.choice(RECOVERY_ALPHABET) for _ in range(16))
    return "-".join(raw[index:index + 4] for index in range(0, 16, 4))


def normalize_recovery_key(value: object) -> str:
    key = str(value or "").strip().upper()
    if not RECOVERY_KEY_RE.fullmatch(key):
        raise DomainError("recovery key must use the format XXXX-XXXX-XXXX-XXXX")
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
