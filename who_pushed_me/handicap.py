from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from who_pushed_me.domain import DomainError


def normalize_handicap_index(value: object | None) -> float | None:
    if value in (None, ""):
        return None
    try:
        index = Decimal(str(value))
    except Exception as error:
        raise DomainError("handicap index must be between -10.0 and 54.0") from error
    if index < Decimal("-10.0") or index > Decimal("54.0"):
        raise DomainError("handicap index must be between -10.0 and 54.0")
    return float(index.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def normalize_round_handicap(value: object | None) -> int | None:
    if value in (None, ""):
        return None
    try:
        handicap = int(value)
    except (TypeError, ValueError) as error:
        raise DomainError("round handicap must be between -20 and 80") from error
    if handicap < -20 or handicap > 80:
        raise DomainError("round handicap must be between -20 and 80")
    return handicap


def calculate_course_handicap(
    handicap_index: object,
    slope_rating: object,
    course_rating: object,
    par: object,
) -> int:
    try:
        index = Decimal(str(handicap_index))
        slope = Decimal(str(slope_rating))
        rating = Decimal(str(course_rating))
        course_par = Decimal(str(par))
    except Exception as error:
        raise DomainError("course handicap inputs must be numeric") from error

    if slope < 55 or slope > 155:
        raise DomainError("slope rating must be between 55 and 155")
    if rating < 40 or rating > 100:
        raise DomainError("course rating must be between 40 and 100")
    if course_par <= 0:
        raise DomainError("course par must be positive")

    value = index * slope / Decimal("113") + (rating - course_par)
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
