from __future__ import annotations

from dataclasses import dataclass

from who_pushed_me.domain import DomainError


@dataclass(frozen=True)
class RoutePosition:
    route_position: int
    hole_number: int

    def as_dict(self) -> dict[str, int]:
        return {
            "route_position": self.route_position,
            "hole_number": self.hole_number,
        }


def _course_holes(course_hole_count: object) -> list[int]:
    try:
        count = int(course_hole_count)
    except (TypeError, ValueError) as error:
        raise DomainError("course_hole_count must be 9 or 18") from error

    if count not in {9, 18}:
        raise DomainError("course_hole_count must be 9 or 18")
    return list(range(1, count + 1))


def _start_index(holes: list[int], start_hole: object) -> int:
    try:
        start = int(start_hole)
    except (TypeError, ValueError) as error:
        raise DomainError("start_hole must be a valid course hole") from error

    if start not in holes:
        raise DomainError("start_hole must be a valid course hole")
    return holes.index(start)


def _cyclic_holes(holes: list[int], start_index: int):
    index = start_index
    while True:
        yield holes[index]
        index = (index + 1) % len(holes)


def build_route(
    *,
    course_hole_count: object,
    start_hole: object = 1,
    hole_count: object | None = None,
    end_hole: object | None = None,
) -> list[RoutePosition]:
    """
    Build the exact play order for a round.

    Exactly one of hole_count or end_hole must be supplied.

    hole_count supports wrapped routes and repeated physical holes, e.g.
    a 9-hole course played for 18 holes.

    end_hole stops at the first occurrence of that physical hole while
    moving forward cyclically. If end_hole == start_hole, the route contains
    exactly one hole; a full loop must be expressed with hole_count.
    """
    holes = _course_holes(course_hole_count)
    start_index = _start_index(holes, start_hole)

    if (hole_count is None) == (end_hole is None):
        raise DomainError("choose exactly one of hole_count or end_hole")

    sequence: list[int] = []

    if hole_count is not None:
        try:
            requested = int(hole_count)
        except (TypeError, ValueError) as error:
            raise DomainError("hole_count must be a positive number") from error

        if requested < 1:
            raise DomainError("hole_count must be a positive number")

        iterator = _cyclic_holes(holes, start_index)
        sequence = [next(iterator) for _ in range(requested)]
    else:
        try:
            end = int(end_hole)
        except (TypeError, ValueError) as error:
            raise DomainError("end_hole must be a valid course hole") from error

        if end not in holes:
            raise DomainError("end_hole must be a valid course hole")

        iterator = _cyclic_holes(holes, start_index)
        for _ in range(len(holes)):
            hole = next(iterator)
            sequence.append(hole)
            if hole == end:
                break
        else:
            raise DomainError("could not build route to end_hole")

    return [
        RoutePosition(route_position=index, hole_number=hole)
        for index, hole in enumerate(sequence, start=1)
    ]


def extend_route(
    existing: list[RoutePosition],
    *,
    course_hole_count: object,
    additional_holes: object,
) -> list[RoutePosition]:
    if not existing:
        raise DomainError("existing route cannot be empty")

    try:
        amount = int(additional_holes)
    except (TypeError, ValueError) as error:
        raise DomainError("additional_holes must be a positive number") from error

    if amount < 1:
        raise DomainError("additional_holes must be a positive number")

    holes = _course_holes(course_hole_count)
    last_hole = existing[-1].hole_number
    if last_hole not in holes:
        raise DomainError("existing route contains an invalid physical hole")

    next_index = (holes.index(last_hole) + 1) % len(holes)
    iterator = _cyclic_holes(holes, next_index)

    result = list(existing)
    first_new_position = len(result) + 1
    for offset in range(amount):
        result.append(
            RoutePosition(
                route_position=first_new_position + offset,
                hole_number=next(iterator),
            )
        )
    return result


def build_tracking_plan(
    *,
    route_length: object,
    tracking_start_position: object = 1,
    prior_holes_mode: object = "untracked",
) -> dict[str, object]:
    try:
        length = int(route_length)
        start = int(tracking_start_position)
    except (TypeError, ValueError) as error:
        raise DomainError("tracking route values must be numbers") from error

    if length < 1 or not 1 <= start <= length:
        raise DomainError(
            "tracking_start_position must be within the round route"
        )

    mode = str(prior_holes_mode or "untracked").strip().lower()
    if mode not in {"untracked", "backfill"}:
        raise DomainError(
            "prior_holes_mode must be untracked or backfill"
        )

    skipped_positions = (
        frozenset(range(1, start))
        if mode == "untracked"
        else frozenset()
    )
    return {
        "tracking_start_position": start,
        "prior_holes_mode": mode,
        "participant_tracked_from": (
            start if mode == "untracked" else 1
        ),
        "skipped_positions": skipped_positions,
    }


def route_progress_label(route_position: object, route_length: object) -> str:
    try:
        position = int(route_position)
        length = int(route_length)
    except (TypeError, ValueError) as error:
        raise DomainError("route progress values must be numbers") from error

    if length < 1 or not 1 <= position <= length:
        raise DomainError("route position must be within the route")
    return f"{position} OF {length}"
