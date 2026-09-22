from who_pushed_me.reporting import (
    _content_archive_entries,
    _net_standings_rows,
    _total_par,
    build_round_report_pdf,
)


def test_completed_individual_round_builds_pdf_bytes():
    round_data = {
        "status": "completed",
        "mode": "individual",
        "hole_count": 2,
        "free_play_name": "Saturday Shitshow",
        "course": None,
        "viewer_role": "player",
        "viewer_participant_id": "p1",
        "participants": [
            {"id": "p1", "role": "player", "display_name": "Kim"},
            {"id": "p2", "role": "player", "display_name": "Pat"},
        ],
        "pars": [
            {"hole_number": 1, "par": 4},
            {"hole_number": 2, "par": 3},
        ],
        "scores": [
            {
                "hole_number": 1,
                "score_scope": "player",
                "player_participant_id": "p1",
                "strokes": 5,
            },
            {
                "hole_number": 2,
                "score_scope": "player",
                "player_participant_id": "p1",
                "strokes": 4,
            },
            {
                "hole_number": 1,
                "score_scope": "player",
                "player_participant_id": "p2",
                "strokes": 4,
            },
            {
                "hole_number": 2,
                "score_scope": "player",
                "player_participant_id": "p2",
                "strokes": 3,
            },
        ],
        "contributions": [],
        "results": {
            "mode": "individual",
            "complete": True,
            "team_total": None,
            "players": [
                {
                    "participant_id": "p2",
                    "display_name": "Pat",
                    "score_count": 2,
                    "missing_scores": 0,
                    "total_strokes": 7,
                    "rank": 1,
                    "tie_count": 1,
                },
                {
                    "participant_id": "p1",
                    "display_name": "Kim",
                    "score_count": 2,
                    "missing_scores": 0,
                    "total_strokes": 9,
                    "rank": 2,
                    "tie_count": 1,
                },
            ],
        },
        "events": [
            {
                "event_type": "round_end_result",
                "data": {"player_participant_id": "p1"},
                "presentation": {
                    "fallback": {"text": "Head-to-head loser"},
                    "banter": None,
                    "mascot": None,
                },
            }
        ],
    }

    pdf = build_round_report_pdf(
        round_data,
        preferences={"max_vulgarity": "brutal"},
    )

    assert pdf.startswith(b"%PDF-")
    assert len(pdf) > 1500


def test_completed_scramble_round_builds_pdf_bytes():
    round_data = {
        "status": "completed",
        "mode": "scramble",
        "hole_count": 2,
        "free_play_name": "Team Disaster",
        "course": None,
        "viewer_role": "player",
        "viewer_participant_id": "p1",
        "participants": [
            {"id": "p1", "role": "player", "display_name": "Kim"},
            {"id": "p2", "role": "player", "display_name": "Pat"},
        ],
        "pars": [
            {"hole_number": 1, "par": 4},
            {"hole_number": 2, "par": 4},
        ],
        "scores": [
            {
                "hole_number": 1,
                "score_scope": "team",
                "player_participant_id": None,
                "strokes": 5,
            },
            {
                "hole_number": 2,
                "score_scope": "team",
                "player_participant_id": None,
                "strokes": 6,
            },
        ],
        "contributions": [
            {
                "hole_number": 1,
                "shot_type": "drive",
                "player_participant_id": "p1",
            },
            {
                "hole_number": 1,
                "shot_type": "putt",
                "player_participant_id": "p2",
            },
        ],
        "results": {
            "mode": "scramble",
            "complete": True,
            "team_total": 11,
            "players": [],
        },
        "events": [],
    }

    pdf = build_round_report_pdf(
        round_data,
        preferences={"max_vulgarity": "normal"},
    )

    assert pdf.startswith(b"%PDF-")
    assert len(pdf) > 1500

def test_completed_incomplete_individual_round_still_builds_report():
    round_data = {
        "status": "completed",
        "mode": "individual",
        "hole_count": 2,
        "free_play_name": "Missing Receipt",
        "course": None,
        "viewer_role": "player",
        "viewer_participant_id": "p1",
        "participants": [
            {"id": "p1", "role": "player", "display_name": "Kim"},
        ],
        "pars": [],
        "scores": [
            {
                "hole_number": 1,
                "score_scope": "player",
                "player_participant_id": "p1",
                "strokes": 5,
            },
        ],
        "contributions": [],
        "results": {
            "mode": "individual",
            "complete": False,
            "missing_scores": 1,
            "team_total": None,
            "players": [
                {
                    "participant_id": "p1",
                    "display_name": "Kim",
                    "participation_state": "active",
                    "coverage_state": "incomplete",
                    "required_scores": 2,
                    "score_count": 1,
                    "missing_scores": 1,
                    "total_strokes": 5,
                    "rank": None,
                    "tie_count": 0,
                },
            ],
        },
        "events": [],
    }

    pdf = build_round_report_pdf(round_data)

    assert pdf.startswith(b"%PDF-")
    assert len(pdf) > 1500


def test_completed_incomplete_scramble_round_still_builds_report():
    round_data = {
        "status": "completed",
        "mode": "scramble",
        "hole_count": 2,
        "free_play_name": "Team Missing Receipt",
        "course": None,
        "viewer_role": "player",
        "viewer_participant_id": "p1",
        "participants": [
            {"id": "p1", "role": "player", "display_name": "Kim"},
        ],
        "pars": [],
        "scores": [
            {
                "hole_number": 1,
                "score_scope": "team",
                "player_participant_id": None,
                "strokes": 5,
            },
        ],
        "contributions": [],
        "results": {
            "mode": "scramble",
            "complete": False,
            "score_count": 1,
            "required_scores": 2,
            "missing_scores": 1,
            "team_total": 5,
            "players": [],
        },
        "events": [],
    }

    pdf = build_round_report_pdf(round_data)

    assert pdf.startswith(b"%PDF-")
    assert len(pdf) > 1500


def test_final_report_archive_keeps_every_used_banter_and_mini_occurrence():
    mini_path = (
        "static/assets/mascots/mini/joining/new-player/"
        "WPM_Join_NewPlayer_FirstRoundWithUsPoorBastard.webp"
    )
    round_data = {
        "events": [
            {
                "event_type": "score_push",
                "content_event_key": "score.push.individual.raised",
                "hole_number": 2,
                "data": {},
                "presentation": {
                    "banter": {"text": "Same insult"},
                    "mascot": {
                        "copy": "Mini two",
                        "production": mini_path,
                    },
                },
            },
            {
                "event_type": "score_report",
                "content_event_key": "score.report.individual.bogey",
                "hole_number": 1,
                "data": {"message": "Custom first receipt"},
                "presentation": {
                    "banter": {"text": "Same insult"},
                    "mascot": {
                        "copy": "Mini one",
                        "production": mini_path,
                    },
                },
            },
        ]
    }

    archive = _content_archive_entries(round_data)

    assert len(archive) == 2
    assert [row["hole_number"] for row in archive] == [1, 2]
    assert [row["banter_text"] for row in archive] == [
        "Same insult",
        "Same insult",
    ]
    assert [row["mascot_copy"] for row in archive] == [
        "Mini one",
        "Mini two",
    ]
    assert archive[0]["custom_message"] == "Custom first receipt"
    assert all(row["mascot_path"] == mini_path for row in archive)




def test_net_standings_are_pending_until_every_eligible_handicap_exists():
    round_data = {
        "net_scoring_enabled": True,
        "results": {
            "net_scoring_enabled": True,
            "net_official": False,
            "players": [
                {
                    "display_name": "Kim",
                    "participation_state": "active",
                    "coverage_state": "complete",
                    "rank": 1,
                    "total_strokes": 80,
                    "round_handicap": 10,
                    "net_total_strokes": 70,
                    "net_rank": None,
                    "net_tie_count": 0,
                    "net_placement_eligible": False,
                },
                {
                    "display_name": "Pat",
                    "participation_state": "active",
                    "coverage_state": "complete",
                    "rank": 2,
                    "total_strokes": 82,
                    "round_handicap": None,
                    "net_total_strokes": None,
                    "net_rank": None,
                    "net_tie_count": 0,
                    "net_placement_eligible": False,
                },
            ],
        },
    }

    rows = _net_standings_rows(round_data)

    assert rows[0] == ["Net Place", "Golfer", "Hcp", "Net"]
    assert rows[1] == ["PENDING", "Kim", 10, 70]
    assert rows[2] == ["PENDING", "Pat", "-", "-"]


def test_net_standings_show_rank_only_when_net_is_official():
    round_data = {
        "net_scoring_enabled": True,
        "results": {
            "net_scoring_enabled": True,
            "net_official": True,
            "players": [
                {
                    "display_name": "Kim",
                    "participation_state": "active",
                    "coverage_state": "complete",
                    "rank": 2,
                    "total_strokes": 82,
                    "round_handicap": 14,
                    "net_total_strokes": 68,
                    "net_rank": 1,
                    "net_tie_count": 1,
                    "net_placement_eligible": True,
                },
                {
                    "display_name": "Pat",
                    "participation_state": "active",
                    "coverage_state": "complete",
                    "rank": 1,
                    "total_strokes": 80,
                    "round_handicap": 10,
                    "net_total_strokes": 70,
                    "net_rank": 2,
                    "net_tie_count": 1,
                    "net_placement_eligible": True,
                },
            ],
        },
    }

    rows = _net_standings_rows(round_data)

    assert rows[1] == ["#1", "Kim", 14, 68]
    assert rows[2] == ["#2", "Pat", 10, 70]


def test_total_par_ignores_deliberately_untracked_route_positions():
    round_data = {
        "hole_count": 4,
        "route": [
            {"route_position": 1, "hole_number": 1, "state": "skipped"},
            {"route_position": 2, "hole_number": 2, "state": "skipped"},
            {"route_position": 3, "hole_number": 3, "state": "planned"},
            {"route_position": 4, "hole_number": 4, "state": "planned"},
        ],
        "pars": [
            {"route_position": 3, "hole_number": 3, "par": 4},
            {"route_position": 4, "hole_number": 4, "par": 5},
        ],
    }

    assert _total_par(round_data) == 9


def test_completed_net_individual_round_builds_pdf_bytes():
    round_data = {
        "status": "completed",
        "mode": "individual",
        "hole_count": 2,
        "net_scoring_enabled": True,
        "free_play_name": "Net Evidence",
        "course": None,
        "viewer_role": "player",
        "viewer_participant_id": "p1",
        "participants": [
            {
                "id": "p1",
                "role": "player",
                "display_name": "Kim",
                "round_handicap": 2,
            },
            {
                "id": "p2",
                "role": "player",
                "display_name": "Pat",
                "round_handicap": 0,
            },
        ],
        "pars": [
            {"hole_number": 1, "par": 4},
            {"hole_number": 2, "par": 4},
        ],
        "scores": [
            {
                "hole_number": 1,
                "score_scope": "player",
                "player_participant_id": "p1",
                "strokes": 5,
            },
            {
                "hole_number": 2,
                "score_scope": "player",
                "player_participant_id": "p1",
                "strokes": 5,
            },
            {
                "hole_number": 1,
                "score_scope": "player",
                "player_participant_id": "p2",
                "strokes": 4,
            },
            {
                "hole_number": 2,
                "score_scope": "player",
                "player_participant_id": "p2",
                "strokes": 5,
            },
        ],
        "contributions": [],
        "results": {
            "mode": "individual",
            "complete": True,
            "net_scoring_enabled": True,
            "net_official": True,
            "missing_handicaps": 0,
            "players": [
                {
                    "participant_id": "p1",
                    "display_name": "Kim",
                    "participation_state": "active",
                    "coverage_state": "complete",
                    "required_scores": 2,
                    "score_count": 2,
                    "missing_scores": 0,
                    "total_strokes": 10,
                    "rank": 2,
                    "tie_count": 1,
                    "round_handicap": 2,
                    "net_total_strokes": 8,
                    "net_rank": 1,
                    "net_tie_count": 1,
                    "net_placement_eligible": True,
                },
                {
                    "participant_id": "p2",
                    "display_name": "Pat",
                    "participation_state": "active",
                    "coverage_state": "complete",
                    "required_scores": 2,
                    "score_count": 2,
                    "missing_scores": 0,
                    "total_strokes": 9,
                    "rank": 1,
                    "tie_count": 1,
                    "round_handicap": 0,
                    "net_total_strokes": 9,
                    "net_rank": 2,
                    "net_tie_count": 1,
                    "net_placement_eligible": True,
                },
            ],
        },
        "events": [],
    }

    pdf = build_round_report_pdf(round_data)

    assert pdf.startswith(b"%PDF-")
    assert len(pdf) > 1500
