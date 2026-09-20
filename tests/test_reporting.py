from who_pushed_me.reporting import (
    _content_archive_entries,
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

