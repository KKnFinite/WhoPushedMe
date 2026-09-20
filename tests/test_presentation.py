import random

from who_pushed_me.content.catalog import ContentCatalog
from who_pushed_me.content.presentation import (
    build_shared_presentation,
    filter_presentation_for_preferences,
    par_content_event,
    score_content_event,
    scramble_contribution_content_event,
    score_response_content_event,
    social_content_event,
    status_content_event,
)


def test_score_content_event_classifies_reports_and_pushes():
    assert score_content_event(
        mode="individual",
        old_score=None,
        new_score=3,
        par=4,
        hole_number=5,
        current_hole=5,
    ) == "score.report.individual.birdie"

    assert score_content_event(
        mode="scramble",
        old_score=None,
        new_score=1,
        par=3,
        hole_number=7,
        current_hole=7,
    ) == "score.report.scramble.ace"

    assert score_content_event(
        mode="individual",
        old_score=4,
        new_score=6,
        par=4,
        hole_number=3,
        current_hole=6,
    ) == "score.push.individual.old_hole_raised"

    assert score_content_event(
        mode="scramble",
        old_score=6,
        new_score=5,
        par=4,
        hole_number=6,
        current_hole=6,
    ) == "score.push.scramble.lowered"


def test_other_round_actions_map_to_canonical_content_events():
    assert par_content_event(None, 4) == "par.report"
    assert par_content_event(4, 5) == "par.push.increase"
    assert par_content_event(5, 4) == "par.push.decrease"

    assert status_content_event("setup", "active") == "round.start"
    assert status_content_event("completed", "active") == "round.resume"
    assert status_content_event("active", "completed") == "round.completed"
    assert status_content_event("active", "abandoned") == "round.abandoned"

    assert (
        scramble_contribution_content_event(None, "p1", "drive")
        == "scramble.contribution.drive"
    )
    assert (
        scramble_contribution_content_event("p1", "p2", "drive")
        == "scramble.contribution.changed"
    )


def test_score_responses_map_to_specific_content_events():
    assert score_response_content_event("bullshit") == "score.response.bullshit"
    assert score_response_content_event("cheater") == "score.response.cheater"
    assert score_response_content_event("blame") == "score.response.blame"
    assert score_response_content_event("random") == "score.response.random"
    assert score_response_content_event("wat") == "score.response.random"


def test_social_actions_map_to_specific_mid_hole_events():
    assert (
        social_content_event("callout", {"situation": "water_shot"})
        == "mid_hole.callout.water_shot"
    )
    assert (
        social_content_event("praise", {"shot_type": "long_putt"})
        == "mid_hole.nice_shot.long_putt"
    )
    assert (
        social_content_event("excuse", {"reason": "wind"})
        == "mid_hole.excuse.wind"
    )
    assert (
        social_content_event("reaction", {"reaction": "bullshit"})
        == "mid_hole.reaction.bullshit"
    )
    assert (
        social_content_event("shot_call", {})
        == "mid_hole.call_your_shot.issued"
    )
    assert (
        social_content_event("challenge", {})
        == "mid_hole.you_wont.issued"
    )


def test_shared_everyone_content_is_not_rerolled_for_subject_and_others():
    catalog = ContentCatalog.load()
    presentation = build_shared_presentation(
        catalog,
        "score.push.individual.raised",
        controls={
            "mini_mascots_enabled": True,
            "trash_talk_enabled": True,
            "event_overrides": {},
        },
        rng=random.Random(42),
    )

    variants = presentation["variants"]
    assert {"everyone", "subject", "others"} <= set(variants)

    everyone_mascot = variants["everyone"]["mascot"]["asset_id"]
    assert variants["subject"]["mascot"]["asset_id"] == everyone_mascot
    assert variants["others"]["mascot"]["asset_id"] == everyone_mascot

    everyone_banter = variants["everyone"]["banter"]["id"]
    assert variants["subject"]["banter"]["id"] == everyone_banter
    assert variants["others"]["banter"]["id"] == everyone_banter


def test_admin_disabled_event_keeps_factual_fallback_only():
    catalog = ContentCatalog.load()
    presentation = build_shared_presentation(
        catalog,
        "mid_hole.callout.water_shot",
        controls={
            "mini_mascots_enabled": True,
            "trash_talk_enabled": True,
            "event_overrides": {"mid_hole.callout": False},
        },
        rng=random.Random(1),
    )

    assert presentation["event_key"] == "mid_hole.callout.water_shot"
    assert presentation["fallback"]["text"] == "Water shot"
    assert presentation["variants"] == {}


def test_preferences_filter_stored_selection_without_rerolling():
    presentation = {
        "event_key": "round.end.scramble.complete",
        "fallback": {"text": "Scramble complete"},
        "variants": {
            "everyone": {
                "banter": {
                    "id": "banter.test",
                    "text": "Test",
                    "vulgarity": "brutal",
                    "themes": [],
                    "audiences": ["everyone"],
                },
                "mascot": {
                    "asset_id": "mini.test",
                    "vulgarity": "normal",
                    "themes": ["wife"],
                    "audiences": ["everyone"],
                },
            }
        },
    }

    filtered = filter_presentation_for_preferences(
        presentation,
        {
            "mini_mascots_enabled": True,
            "trash_talk_enabled": True,
            "max_vulgarity": "normal",
            "themes": {"wife": False, "drinking": True},
        },
    )

    assert filtered["fallback"] == {"text": "Scramble complete"}
    assert filtered["banter"] is None
    assert filtered["mascot"] is None
