import pytest

from who_pushed_me.auth import (
    generate_recovery_key,
    generate_session_token,
    hash_password,
    hash_recovery_key,
    hash_session_token,
    normalize_login_username,
    normalize_recovery_key,
    normalize_username,
    validate_password,
    verify_password,
)
from who_pushed_me.domain import DomainError


def test_username_is_normalized_and_case_insensitive():
    assert normalize_username("  Khris.K  ") == "khris.k"


@pytest.mark.parametrize(
    "value",
    ["ab", "bad name", "@name", "a" * 17],
)
def test_username_rejects_invalid_values(value):
    with pytest.raises(DomainError):
        normalize_username(value)


def test_legacy_username_length_can_still_log_in():
    assert normalize_login_username("a" * 24) == "a" * 24
    with pytest.raises(DomainError):
        normalize_username("a" * 24)


@pytest.mark.parametrize(
    "value",
    [
        "1234567890",
        "aaaaaaaaaa",
        "abcdefghij",
        "password123",
        "basketball",
        "abcdefghijk",
    ],
)
def test_new_password_policy_rejects_obvious_passwords(value):
    with pytest.raises(DomainError):
        validate_password(value)


def test_new_password_policy_allows_spaces_and_password_manager_style_values():
    assert validate_password("correct horse battery staple") == "correct horse battery staple"
    assert validate_password("gB7!pQ2#xL9@") == "gB7!pQ2#xL9@"


def test_password_hash_round_trip_does_not_store_plaintext():
    encoded = hash_password("correct horse battery staple")

    assert "correct horse battery staple" not in encoded
    assert verify_password(encoded, "correct horse battery staple")
    assert not verify_password(encoded, "wrong password")


def test_recovery_key_is_current_eight_character_format_and_hashable():
    key = generate_recovery_key()

    assert len(key) == 9
    assert normalize_recovery_key(key.lower()) == key
    assert len(hash_recovery_key(key)) == 64


def test_legacy_recovery_keys_remain_accepted_for_existing_accounts():
    legacy = "ABCD-EFGH-JKMP-QRST"
    assert normalize_recovery_key(legacy.lower()) == legacy


def test_session_tokens_are_random_and_stored_as_hashes():
    first = generate_session_token()
    second = generate_session_token()

    assert first != second
    assert len(first) >= 32
    assert len(hash_session_token(first)) == 64
    assert hash_session_token(first) != hash_session_token(second)
