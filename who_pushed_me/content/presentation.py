from __future__ import annotations

import random
from typing import Any, Mapping

from who_pushed_me.content.catalog import (
    ALLOWED_PLACEHOLDERS,
    ContentCatalog,
    VULGARITY_ORDER,
)
from who_pushed_me.content.preferences import blocked_themes


_SCORE_NAMES = {
    -2: "eagle",
    -1: "birdie",
    0: "par",
    1: "bogey",
    2: "double_bogey",
    3: "triple_bogey",
}

_CALLOUT_SITUATIONS = {
    "water_shot",
    "out_of_bounds",
    "lost_ball",
    "tree_shot",
    "bunker",
    "cart_path",
    "shank",
    "slice",
    "hook",
    "topped",
    "chunked",
    "bladed",
    "duff",
    "whiff",
    "penalty",
    "mulligan",
    "foot_wedge",
    "wrong_club",
    "way_short",
    "way_long",
    "slow_play",
    "missed_short_putt",
    "three_putt",
    "lip_out",
}

_NICE_SHOT_TYPES = {
    "drive",
    "approach",
    "recovery",
    "bunker",
    "putt",
    "long_putt",
}

_EXCUSE_REASONS = {
    "clubs",
    "wind",
    "weather",
    "bad_lie",
    "green",
    "noise",
    "alcohol",
    "hangover",
    "pace",
}

_REACTIONS = {"laugh", "bullshit", "applause"}

_SCORE_RESPONSES = {
    "bullshit",
    "cheater",
    "lucky",
    "nice",
    "blame",
    "random",
    "custom",
}

_CONTRIBUTION_TYPES = {
    "drive",
    "second",
    "approach",
    "recovery",
    "bunker",
    "putt",
    "other",
}


def score_content_event(
    *,
    mode: str,
    old_score: int | None,
    new_score: int,
    par: int | None,
    hole_number: int,
    current_hole: int,
) -> str:
    scope = "scramble" if mode == "scramble" else "individual"

    if old_score is None:
        base = f"score.report.{scope}"
        if par is None:
            return base
        if new_score == 1:
            return f"{base}.ace"
        delta = new_score - par
        if delta <= -3:
            score_name = "albatross"
        elif delta >= 4:
            score_name = "quad_plus"
        else:
            score_name = _SCORE_NAMES[delta]
        return f"{base}.{score_name}"

    direction = "lowered" if new_score < old_score else "raised"
    old_hole = hole_number < current_hole
    suffix = f"old_hole_{direction}" if old_hole else direction
    return f"score.push.{scope}.{suffix}"


def par_content_event(old_par: int | None, new_par: int) -> str:
    if old_par is None:
        return "par.report"
    return "par.push.increase" if new_par > old_par else "par.push.decrease"


def status_content_event(old_status: str, new_status: str) -> str | None:
    if new_status == "active":
        return "round.start" if old_status == "setup" else "round.resume"
    if new_status == "completed":
        return "round.completed"
    if new_status == "abandoned":
        return "round.abandoned"
    return None


def score_response_content_event(response_kind: object) -> str:
    kind = str(response_kind or "").strip().lower()
    if kind not in _SCORE_RESPONSES:
        kind = "random"
    return f"score.response.{kind}"


def scramble_contribution_content_event(
    old_target: object | None,
    new_target: object | None,
    shot_type: str,
) -> str:
    if old_target is not None or new_target is None:
        return "scramble.contribution.changed"
    kind = shot_type if shot_type in _CONTRIBUTION_TYPES else "other"
    return f"scramble.contribution.{kind}"


def social_content_event(kind: str, payload: Mapping[str, object]) -> str:
    if kind == "callout":
        situation = str(payload.get("situation") or "").strip().lower()
        if situation in _CALLOUT_SITUATIONS:
            return f"mid_hole.callout.{situation}"
        return "mid_hole.callout"

    if kind == "praise":
        shot_type = str(payload.get("shot_type") or "").strip().lower()
        if shot_type in _NICE_SHOT_TYPES:
            return f"mid_hole.nice_shot.{shot_type}"
        return "mid_hole.nice_shot"

    if kind == "excuse":
        reason = str(payload.get("reason") or "").strip().lower()
        if reason in _EXCUSE_REASONS:
            return f"mid_hole.excuse.{reason}"
        return "mid_hole.excuse"

    if kind == "reaction":
        reaction = str(payload.get("reaction") or "").strip().lower()
        if reaction in _REACTIONS:
            return f"mid_hole.reaction.{reaction}"
        return "mid_hole.reaction"

    return {
        "open_mic": "mid_hole.open_mic",
        "shot_call": "mid_hole.call_your_shot.issued",
        "challenge": "mid_hole.you_wont.issued",
    }[kind]


def _render_context(context: Mapping[str, object] | None) -> dict[str, object]:
    result = {key: "" for key in ALLOWED_PLACEHOLDERS}
    result.update(dict(context or {}))
    return result


def _content_item(row: Mapping[str, Any] | None, *, text: str | None = None) -> dict[str, Any] | None:
    if row is None:
        return None
    item = {
        "vulgarity": str(row.get("vulgarity") or "normal"),
        "themes": list(row.get("themes") or []),
        "audiences": list(row.get("audiences") or ["everyone"]),
    }
    if "id" in row:
        item["id"] = row["id"]
    if "asset_id" in row:
        item["asset_id"] = row["asset_id"]
    if text is not None:
        item["text"] = text
    if row.get("copy"):
        item["copy"] = row["copy"]
    if row.get("hat_copy"):
        item["hat_copy"] = row["hat_copy"]
    return item


def _content_identity(row: Mapping[str, Any] | None) -> tuple[str, object] | None:
    if row is None:
        return None
    if "id" in row:
        return ("id", row["id"])
    if "asset_id" in row:
        return ("asset_id", row["asset_id"])
    return None


def _audience_choice(
    choices: list[dict[str, Any]],
    audience: str,
    shared: Mapping[str, Any] | None,
    *,
    picker: Any,
) -> dict[str, Any] | None:
    explicit = [
        row
        for row in choices
        if audience in set(row.get("audiences") or ["everyone"])
        and "everyone" not in set(row.get("audiences") or ["everyone"])
    ]
    if explicit:
        return picker.choice(explicit)

    shared_identity = _content_identity(shared)
    if shared_identity is not None:
        for row in choices:
            if _content_identity(row) == shared_identity:
                return row

    everyone = [
        row
        for row in choices
        if "everyone" in set(row.get("audiences") or ["everyone"])
    ]
    return picker.choice(everyone or choices) if choices else None


def build_shared_presentation(
    catalog: ContentCatalog,
    event_key: str,
    *,
    controls: Mapping[str, Any],
    context: Mapping[str, object] | None = None,
    rng: random.Random | None = None,
) -> dict[str, Any]:
    canonical = catalog.registry.canonical_key(event_key)
    event = catalog.registry.event(canonical)
    overrides = dict(controls.get("event_overrides") or {})
    fallback = {
        "text": str(event.get("label") or canonical),
    }
    presentation: dict[str, Any] = {
        "event_key": canonical,
        "fallback": fallback,
        "variants": {},
    }

    if not catalog.registry.is_enabled(canonical, overrides):
        return presentation

    audiences = ["everyone"]
    for audience in event.get("audiences") or []:
        if audience not in audiences:
            audiences.append(audience)

    render_context = _render_context(context)
    mini_assets = {
        row["asset_id"]: row
        for row in catalog.asset_manifest.get("assets", [])
        if row.get("family") == "mini-mascot"
    }
    picker = rng or random

    shared_banter = None
    if bool(controls.get("trash_talk_enabled", True)):
        shared_banter = catalog.choose_banter(
            canonical,
            audience="everyone",
            admin_overrides=overrides,
            rng=rng,
        )

    shared_mascot = None
    if bool(controls.get("mini_mascots_enabled", True)):
        shared_mascot = catalog.choose_mascot(
            canonical,
            audience="everyone",
            admin_overrides=overrides,
            rng=rng,
        )

    for audience in audiences:
        banter_row = None
        mascot_row = None

        if bool(controls.get("trash_talk_enabled", True)):
            choices = catalog.eligible_banter(
                canonical,
                audience=audience,
                admin_overrides=overrides,
            )
            banter_row = (
                shared_banter
                if audience == "everyone"
                else _audience_choice(
                    choices,
                    audience,
                    shared_banter,
                    picker=picker,
                )
            )

        if bool(controls.get("mini_mascots_enabled", True)):
            choices = catalog.eligible_mascots(
                canonical,
                audience=audience,
                admin_overrides=overrides,
            )
            mascot_row = (
                shared_mascot
                if audience == "everyone"
                else _audience_choice(
                    choices,
                    audience,
                    shared_mascot,
                    picker=picker,
                )
            )

        banter = None
        if banter_row is not None:
            banter = _content_item(
                banter_row,
                text=catalog.render_banter(banter_row, render_context),
            )

        mascot = None
        if mascot_row is not None:
            mascot = _content_item(mascot_row)
            asset = mini_assets.get(mascot_row["asset_id"])
            if mascot is not None and asset is not None:
                mascot["production"] = asset.get("production")

        if banter is not None or mascot is not None:
            presentation["variants"][audience] = {
                "banter": banter,
                "mascot": mascot,
            }

    return presentation


def _item_allowed(
    item: Mapping[str, Any] | None,
    *,
    max_vulgarity: str,
    blocked: set[str],
) -> bool:
    if item is None:
        return False
    vulgarity = str(item.get("vulgarity") or "normal")
    if VULGARITY_ORDER[vulgarity] > VULGARITY_ORDER[max_vulgarity]:
        return False
    return not blocked.intersection(item.get("themes") or [])


def filter_presentation_for_preferences(
    presentation: Mapping[str, Any],
    preferences: Mapping[str, Any],
    *,
    audience: str = "everyone",
) -> dict[str, Any]:
    variants = dict(presentation.get("variants") or {})
    variant = dict(variants.get(audience) or variants.get("everyone") or {})
    max_vulgarity = str(preferences.get("max_vulgarity") or "normal")
    blocked = set(blocked_themes(preferences))

    banter = variant.get("banter")
    mascot = variant.get("mascot")

    if not bool(preferences.get("trash_talk_enabled", True)):
        banter = None
    elif not _item_allowed(
        banter,
        max_vulgarity=max_vulgarity,
        blocked=blocked,
    ):
        banter = None

    if not bool(preferences.get("mini_mascots_enabled", True)):
        mascot = None
    elif not _item_allowed(
        mascot,
        max_vulgarity=max_vulgarity,
        blocked=blocked,
    ):
        mascot = None

    return {
        "event_key": presentation.get("event_key"),
        "fallback": dict(presentation.get("fallback") or {}),
        "banter": banter,
        "mascot": mascot,
    }
