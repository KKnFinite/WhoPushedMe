from who_pushed_me.content.derived import (
    score_transition_events,
    standing_transition_events,
)


def row(hole, strokes, par):
    return {
        "hole_number": hole,
        "strokes": strokes,
        "par": par,
    }


def test_first_birdie_and_eagle_fire_on_transition():
    assert score_transition_events([], [row(1, 3, 4)]) == [
        "score.derived.first_birdie"
    ]
    assert score_transition_events([], [row(1, 3, 5)]) == [
        "score.derived.first_eagle"
    ]


def test_birdie_and_bogey_streaks_fire_when_newly_created():
    before = [
        row(1, 3, 4),
        row(2, 3, 4),
        row(3, 4, 4),
    ]
    after = [
        row(1, 3, 4),
        row(2, 3, 4),
        row(3, 3, 4),
    ]

    events = score_transition_events(before, after)
    assert "score.derived.back_to_back_birdies" not in events
    assert "score.derived.birdie_streak_3_plus" in events

    bogey_before = [
        row(1, 5, 4),
        row(2, 5, 4),
        row(3, 4, 4),
    ]
    bogey_after = [
        row(1, 5, 4),
        row(2, 5, 4),
        row(3, 5, 4),
    ]
    assert (
        "score.derived.bogey_streak_3_plus"
        in score_transition_events(bogey_before, bogey_after)
    )


def test_blowup_event_fires_when_score_becomes_quad_plus():
    before = [row(8, 7, 4)]
    after = [row(8, 8, 4)]

    assert score_transition_events(before, after) == [
        "score.derived.blowup_hole"
    ]


def test_leader_and_last_transitions_are_derived_from_completed_standings():
    before = {
        "through_hole": 3,
        "player_count": 3,
        "leaders": {"a"},
        "last": {"c"},
    }
    after = {
        "through_hole": 4,
        "player_count": 3,
        "leaders": {"b"},
        "last": {"a"},
    }

    assert set(standing_transition_events(before, after)) == {
        ("score.derived.new_leader", "b"),
        ("score.derived.lost_lead", "a"),
        ("score.derived.entered_last", "a"),
        ("score.derived.escaped_last", "c"),
    }


def test_first_completed_hole_does_not_spam_tied_lead():
    after = {
        "through_hole": 1,
        "player_count": 4,
        "leaders": {"a", "b", "c", "d"},
        "last": {"a", "b", "c", "d"},
    }

    assert standing_transition_events(None, after) == []
