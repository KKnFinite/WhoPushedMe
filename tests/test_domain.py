import re

import pytest

from who_pushed_me.domain import (
    PermissionDenied,
    audit_event_type,
    generate_recovery_key,
    normalize_shot_type,
    require_active_round,
    require_player,
    validate_shared_hole_change,
    validate_social_event,
)


def test_recovery_keys_are_unambiguous_and_formatted():
    for _ in range(100):
        key = generate_recovery_key()
        assert re.fullmatch(r"[A-HJ-KM-NP-Z2-9]{3}-[A-HJ-KM-NP-Z2-9]{3}", key)
        assert not set(key) & set("O0I1L")


def test_first_value_is_report_and_change_is_push():
    assert audit_event_type("score", None) == "score_report"
    assert audit_event_type("score", 4) == "score_push"
    assert audit_event_type("par", None) == "par_report"
    assert audit_event_type("par", 4) == "par_push"


def test_spectators_only_get_non_shot_specific_social_events():
    assert validate_social_event("spectator", "reaction") == "reaction"
    assert validate_social_event("spectator", "open_mic") == "open_mic"
    for event_type in ("callout", "praise", "excuse", "shot_call", "challenge"):
        with pytest.raises(PermissionDenied):
            validate_social_event("spectator", event_type)
    with pytest.raises(PermissionDenied):
        require_player("spectator", "change scores")


def test_scramble_shot_types_are_flexible_but_normalized():
    assert normalize_shot_type("Drive") == "drive"
    assert normalize_shot_type("Punch-out recovery") == "punch-out_recovery"

def test_round_mutations_require_active_status():
    require_active_round("active", "change scores")
    with pytest.raises(Exception, match="round must be active"):
        require_active_round("completed", "change scores")
    with pytest.raises(Exception, match="round must be active"):
        require_active_round("setup", "change par")


def test_shared_current_hole_never_moves_backward():
    assert validate_shared_hole_change(4, 4) == 4
    assert validate_shared_hole_change(4, 5) == 5
    with pytest.raises(Exception, match="cannot move backward"):
        validate_shared_hole_change(4, 3)

