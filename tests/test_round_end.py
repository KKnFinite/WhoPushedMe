from who_pushed_me.store import RoundStore


def result(total, rank, tie_count):
    return {
        "total_strokes": total,
        "rank": rank,
        "tie_count": tie_count,
    }


def test_two_player_individual_uses_head_to_head_loser():
    results = [
        result(80, 1, 1),
        result(88, 2, 1),
    ]

    assert (
        RoundStore._individual_round_end_event(results[0], results)
        == "round.end.individual.winner"
    )
    assert (
        RoundStore._individual_round_end_event(results[1], results)
        == "round.end.individual.head_to_head_loser"
    )


def test_three_and_four_player_routes_not_last_and_dead_last():
    three = [
        result(80, 1, 1),
        result(85, 2, 1),
        result(92, 3, 1),
    ]
    assert (
        RoundStore._individual_round_end_event(three[1], three)
        == "round.end.individual.not_last"
    )
    assert (
        RoundStore._individual_round_end_event(three[2], three)
        == "round.end.individual.dead_last"
    )

    four = [
        result(80, 1, 1),
        result(84, 2, 1),
        result(87, 3, 1),
        result(91, 4, 1),
    ]
    assert (
        RoundStore._individual_round_end_event(four[1], four)
        == "round.end.individual.not_last"
    )
    assert (
        RoundStore._individual_round_end_event(four[2], four)
        == "round.end.individual.not_last"
    )
    assert (
        RoundStore._individual_round_end_event(four[3], four)
        == "round.end.individual.dead_last"
    )


def test_ties_use_existing_tie_aware_round_end_events():
    tied_first = [
        result(80, 1, 2),
        result(80, 1, 2),
        result(90, 3, 1),
    ]
    assert (
        RoundStore._individual_round_end_event(tied_first[0], tied_first)
        == "round.end.individual.co_winner"
    )

    tied_last = [
        result(80, 1, 1),
        result(90, 2, 2),
        result(90, 2, 2),
    ]
    assert (
        RoundStore._individual_round_end_event(tied_last[1], tied_last)
        == "round.end.individual.tied_last"
    )

    tied_middle = [
        result(80, 1, 1),
        result(85, 2, 2),
        result(85, 2, 2),
        result(95, 4, 1),
    ]
    assert (
        RoundStore._individual_round_end_event(tied_middle[1], tied_middle)
        == "round.end.individual.tied_middle"
    )



def test_live_standings_follow_planned_route_when_tracking_starts_late():
    players = [
        {"participant_id": "p1", "display_name": "Kim"},
        {"participant_id": "p2", "display_name": "Pat"},
    ]
    score_rows = [
        {"player_participant_id": "p1", "route_position": 11, "strokes": 5},
        {"player_participant_id": "p2", "route_position": 11, "strokes": 4},
        {"player_participant_id": "p1", "route_position": 12, "strokes": 4},
        {"player_participant_id": "p2", "route_position": 12, "strokes": 5},
    ]

    state = RoundStore._standing_state_from_rows(
        [11, 12, 13, 14],
        players,
        score_rows,
    )

    assert state is not None
    assert state["through_hole"] == 12
    assert state["totals"] == {"p1": 9, "p2": 9}
    assert state["leaders"] == {"p1", "p2"}
    assert state["last"] == {"p1", "p2"}


def test_live_standings_stop_at_first_missing_planned_position():
    players = [
        {"participant_id": "p1", "display_name": "Kim"},
        {"participant_id": "p2", "display_name": "Pat"},
    ]
    score_rows = [
        {"player_participant_id": "p1", "route_position": 11, "strokes": 5},
        {"player_participant_id": "p2", "route_position": 11, "strokes": 4},
        {"player_participant_id": "p1", "route_position": 13, "strokes": 3},
        {"player_participant_id": "p2", "route_position": 13, "strokes": 6},
    ]

    state = RoundStore._standing_state_from_rows(
        [11, 12, 13],
        players,
        score_rows,
    )

    assert state is not None
    assert state["through_hole"] == 11
    assert state["totals"] == {"p1": 5, "p2": 4}
    assert state["leaders"] == {"p2"}
    assert state["last"] == {"p1"}
