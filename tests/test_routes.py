import pytest

from who_pushed_me.domain import DomainError
from who_pushed_me.routes import (
    build_route,
    build_tracking_plan,
    extend_route,
    route_progress_label,
)


def physical(route):
    return [row.hole_number for row in route]


def test_full_18_can_start_on_any_hole_and_wrap():
    route = build_route(
        course_hole_count=18,
        start_hole=4,
        hole_count=18,
    )

    assert physical(route) == list(range(4, 19)) + [1, 2, 3]
    assert route[0].route_position == 1
    assert route[-1].route_position == 18


def test_custom_end_wraps_and_same_start_end_means_one_hole():
    route = build_route(
        course_hole_count=18,
        start_hole=15,
        end_hole=4,
    )
    assert physical(route) == [15, 16, 17, 18, 1, 2, 3, 4]

    one_hole = build_route(
        course_hole_count=18,
        start_hole=4,
        end_hole=4,
    )
    assert physical(one_hole) == [4]


def test_nine_hole_course_can_be_played_twice_without_overwriting_holes():
    route = build_route(
        course_hole_count=9,
        start_hole=1,
        hole_count=18,
    )

    assert physical(route) == list(range(1, 10)) * 2
    assert route[2].hole_number == 3
    assert route[11].hole_number == 3
    assert route[2].route_position == 3
    assert route[11].route_position == 12


def test_route_extension_appends_new_route_positions():
    route = build_route(
        course_hole_count=9,
        start_hole=1,
        hole_count=9,
    )

    extended = extend_route(
        route,
        course_hole_count=9,
        additional_holes=9,
    )

    assert physical(extended) == list(range(1, 10)) * 2
    assert extended[-1].route_position == 18


def test_progress_label_disambiguates_repeated_physical_holes():
    assert route_progress_label(3, 18) == "3 OF 18"
    assert route_progress_label(12, 18) == "12 OF 18"


def test_route_requires_one_length_strategy():
    with pytest.raises(DomainError, match="exactly one"):
        build_route(
            course_hole_count=18,
            start_hole=1,
        )

    with pytest.raises(DomainError, match="exactly one"):
        build_route(
            course_hole_count=18,
            start_hole=1,
            hole_count=9,
            end_hole=9,
        )



def test_tracking_start_can_leave_prior_route_positions_untracked():
    plan = build_tracking_plan(
        route_length=18,
        tracking_start_position=11,
        prior_holes_mode="untracked",
    )

    assert plan["tracking_start_position"] == 11
    assert plan["participant_tracked_from"] == 11
    assert plan["skipped_positions"] == frozenset(range(1, 11))


def test_tracking_start_can_keep_prior_positions_for_backfill():
    plan = build_tracking_plan(
        route_length=18,
        tracking_start_position=11,
        prior_holes_mode="backfill",
    )

    assert plan["tracking_start_position"] == 11
    assert plan["participant_tracked_from"] == 1
    assert plan["skipped_positions"] == frozenset()


def test_tracking_start_must_be_inside_route():
    with pytest.raises(DomainError, match="within the round route"):
        build_tracking_plan(
            route_length=9,
            tracking_start_position=10,
            prior_holes_mode="untracked",
        )
