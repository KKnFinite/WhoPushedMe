from __future__ import annotations

from typing import Any, Mapping, Sequence


def _score_kind(row: Mapping[str, Any]) -> str | None:
    if row.get("par") is None:
        return None

    strokes = int(row["strokes"])
    par = int(row["par"])
    delta = strokes - par

    if delta == -2:
        return "eagle"
    if delta == -1:
        return "birdie"
    if delta >= 4:
        return "blowup"
    if delta >= 1:
        return "bogey_or_worse"
    return "other"


def _holes_with_kind(
    rows: Sequence[Mapping[str, Any]],
    *kinds: str,
) -> set[int]:
    wanted = set(kinds)
    return {
        int(row["hole_number"])
        for row in rows
        if _score_kind(row) in wanted
    }


def _consecutive_endings(holes: set[int], length: int) -> set[int]:
    if length <= 1:
        return set(holes)
    return {
        hole
        for hole in holes
        if all((hole - offset) in holes for offset in range(length))
    }


def score_transition_events(
    before_rows: Sequence[Mapping[str, Any]],
    after_rows: Sequence[Mapping[str, Any]],
) -> list[str]:
    before_birdies = _holes_with_kind(before_rows, "birdie")
    after_birdies = _holes_with_kind(after_rows, "birdie")

    before_eagles = _holes_with_kind(before_rows, "eagle")
    after_eagles = _holes_with_kind(after_rows, "eagle")

    before_bogeys = _holes_with_kind(before_rows, "bogey_or_worse", "blowup")
    after_bogeys = _holes_with_kind(after_rows, "bogey_or_worse", "blowup")

    before_blowups = _holes_with_kind(before_rows, "blowup")
    after_blowups = _holes_with_kind(after_rows, "blowup")

    events: list[str] = []

    if not before_birdies and after_birdies:
        events.append("score.derived.first_birdie")

    if not before_eagles and after_eagles:
        events.append("score.derived.first_eagle")

    if (
        _consecutive_endings(after_birdies, 2)
        - _consecutive_endings(before_birdies, 2)
    ):
        events.append("score.derived.back_to_back_birdies")

    if (
        _consecutive_endings(after_birdies, 3)
        - _consecutive_endings(before_birdies, 3)
    ):
        events.append("score.derived.birdie_streak_3_plus")

    if (
        _consecutive_endings(after_bogeys, 3)
        - _consecutive_endings(before_bogeys, 3)
    ):
        events.append("score.derived.bogey_streak_3_plus")

    if after_blowups - before_blowups:
        events.append("score.derived.blowup_hole")

    return events


def standing_transition_events(
    before: Mapping[str, Any] | None,
    after: Mapping[str, Any] | None,
) -> list[tuple[str, str]]:
    if not after:
        return []

    after_leaders = set(after.get("leaders") or [])
    after_last = set(after.get("last") or [])
    player_count = int(after.get("player_count") or 0)

    before_leaders = set(before.get("leaders") or []) if before else set()
    before_last = set(before.get("last") or []) if before else set()

    events: list[tuple[str, str]] = []

    if len(after_leaders) == 1:
        leader = next(iter(after_leaders))
        if leader not in before_leaders:
            events.append(("score.derived.new_leader", leader))
    elif before is not None and len(after_leaders) > 1:
        for participant_id in sorted(after_leaders - before_leaders):
            events.append(("score.derived.tied_lead", participant_id))

    if before is not None:
        for participant_id in sorted(before_leaders - after_leaders):
            events.append(("score.derived.lost_lead", participant_id))

    if player_count > 1 and len(after_last) < player_count:
        for participant_id in sorted(after_last - before_last):
            events.append(("score.derived.entered_last", participant_id))

    if (
        before is not None
        and int(before.get("player_count") or 0) > 1
        and len(before_last) < int(before.get("player_count") or 0)
    ):
        for participant_id in sorted(before_last - after_last):
            events.append(("score.derived.escaped_last", participant_id))

    return events
