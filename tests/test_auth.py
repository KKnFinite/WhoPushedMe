import pytest

from who_pushed_me.auth import (
    generate_recovery_key,
    generate_session_token,
    hash_password,
    hash_recovery_key,
    hash_session_token,
    normalize_recovery_key,
    normalize_username,
    verify_password,
)
from who_pushed_me.domain import DomainError


def test_username_is_normalized_and_case_insensitive():
    assert normalize_username("  Khris.K  ") == "khris.k"


@pytest.mark.parametrize(
    "value",
    ["ab", "bad name", "@name", "a" * 25],
)
def test_username_rejects_invalid_values(value):
    with pytest.raises(DomainError):
        normalize_username(value)


def test_password_hash_round_trip_does_not_store_plaintext():
    encoded = hash_password("correct horse battery staple")

    assert "correct horse battery staple" not in encoded
    assert verify_password(encoded, "correct horse battery staple")
    assert not verify_password(encoded, "wrong password")


def test_recovery_key_is_high_entropy_grouped_and_hashable():
    key = generate_recovery_key()

    assert len(key) == 19
    assert normalize_recovery_key(key.lower()) == key
    assert len(hash_recovery_key(key)) == 64


def test_session_tokens_are_random_and_stored_as_hashes():
    first = generate_session_token()
    second = generate_session_token()

    assert first != second
    assert len(first) >= 32
    assert len(hash_session_token(first)) == 64
    assert hash_session_token(first) != hash_session_token(second)
