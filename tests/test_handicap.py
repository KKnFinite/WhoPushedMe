import pytest

from who_pushed_me.domain import DomainError
from who_pushed_me.handicap import (
    calculate_course_handicap,
    normalize_handicap_index,
    normalize_round_handicap,
)


def test_course_handicap_uses_rating_slope_and_par():
    assert calculate_course_handicap(10.0, 125, 72.4, 72) == 11


def test_course_handicap_supports_plus_handicap():
    assert calculate_course_handicap(-2.4, 113, 72.0, 72) == -2


def test_handicap_inputs_are_normalized_and_bounded():
    assert normalize_handicap_index("12.34") == 12.3
    assert normalize_handicap_index("") is None
    assert normalize_round_handicap("-2") == -2
    assert normalize_round_handicap(None) is None

    with pytest.raises(DomainError, match="handicap index"):
        normalize_handicap_index(55)

    with pytest.raises(DomainError, match="round handicap"):
        normalize_round_handicap(81)
