from __future__ import annotations

from typing import Any, Mapping, Sequence

from who_pushed_me.content.catalog import ContentError, VULGARITY_ORDER

DEFAULT_MINI_MASCOTS_ENABLED = True
DEFAULT_TRASH_TALK_ENABLED = True
DEFAULT_MAX_VULGARITY = "brutal"

_ALLOWED_PATCH_KEYS = {
    "mini_mascots_enabled",
    "trash_talk_enabled",
    "max_vulgarity",
    "themes",
}


def _toggleable_themes(theme_rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(row["key"]): dict(row)
        for row in theme_rows
        if bool(row.get("user_toggle", False))
    }


def public_preferences(
    stored: Mapping[str, Any] | None,
    theme_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    row = dict(stored or {})
    theme_definitions = _toggleable_themes(theme_rows)
    overrides = dict(row.get("theme_preferences") or {})

    themes = {
        key: bool(overrides.get(key, definition.get("default_enabled", True)))
        for key, definition in theme_definitions.items()
    }

    return {
        "mini_mascots_enabled": bool(
            row.get("mini_mascots_enabled", DEFAULT_MINI_MASCOTS_ENABLED)
        ),
        "trash_talk_enabled": bool(
            row.get("trash_talk_enabled", DEFAULT_TRASH_TALK_ENABLED)
        ),
        "max_vulgarity": str(
            row.get("max_vulgarity") or DEFAULT_MAX_VULGARITY
        ),
        "themes": themes,
    }


def merge_preference_patch(
    stored: Mapping[str, Any] | None,
    patch: Mapping[str, Any],
    theme_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    unknown = set(patch) - _ALLOWED_PATCH_KEYS
    if unknown:
        raise ContentError(
            "unknown preference fields: " + ", ".join(sorted(unknown))
        )

    current = dict(stored or {})
    result = {
        "mini_mascots_enabled": bool(
            current.get("mini_mascots_enabled", DEFAULT_MINI_MASCOTS_ENABLED)
        ),
        "trash_talk_enabled": bool(
            current.get("trash_talk_enabled", DEFAULT_TRASH_TALK_ENABLED)
        ),
        "max_vulgarity": str(
            current.get("max_vulgarity") or DEFAULT_MAX_VULGARITY
        ),
        "theme_preferences": dict(current.get("theme_preferences") or {}),
    }

    for field in ("mini_mascots_enabled", "trash_talk_enabled"):
        if field in patch:
            value = patch[field]
            if not isinstance(value, bool):
                raise ContentError(f"{field} must be true or false")
            result[field] = value

    if "max_vulgarity" in patch:
        value = str(patch["max_vulgarity"] or "").lower()
        if value not in VULGARITY_ORDER:
            raise ContentError("max_vulgarity must be normal or brutal")
        result["max_vulgarity"] = value

    if "themes" in patch:
        values = patch["themes"]
        if not isinstance(values, Mapping):
            raise ContentError("themes must be an object of theme booleans")

        allowed = _toggleable_themes(theme_rows)
        for key, value in values.items():
            if key not in allowed:
                raise ContentError(f"unknown user-toggleable theme: {key}")
            if not isinstance(value, bool):
                raise ContentError(f"theme {key} must be true or false")
            result["theme_preferences"][key] = value

    return result


def blocked_themes(preferences: Mapping[str, Any]) -> list[str]:
    themes = preferences.get("themes") or {}
    return sorted(
        str(key)
        for key, enabled in themes.items()
        if enabled is False
    )
