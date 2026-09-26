import pytest

from who_pushed_me.content.catalog import ContentCatalog, ContentError
from who_pushed_me.content.preferences import (
    blocked_themes,
    merge_preference_patch,
    public_preferences,
)


def test_content_preferences_default_to_enabled_themes():
    catalog = ContentCatalog.load()
    prefs = public_preferences(None, catalog.theme_rows)

    assert prefs == {
        "mini_mascots_enabled": True,
        "trash_talk_enabled": True,
        "themes": {
            "drinking": True,
            "wife": True,
        },
    }


def test_content_preferences_patch_is_data_driven_and_partial():
    catalog = ContentCatalog.load()
    stored = merge_preference_patch(
        None,
        {
            "mini_mascots_enabled": False,
            "themes": {"drinking": False},
        },
        catalog.theme_rows,
    )
    prefs = public_preferences(stored, catalog.theme_rows)

    assert prefs["mini_mascots_enabled"] is False
    assert prefs["trash_talk_enabled"] is True
    assert "max_vulgarity" not in prefs
    assert prefs["themes"] == {
        "drinking": False,
        "wife": True,
    }
    assert blocked_themes(prefs) == ["drinking"]


def test_content_preferences_reject_unknown_theme():
    catalog = ContentCatalog.load()

    with pytest.raises(ContentError, match="unknown user-toggleable theme"):
        merge_preference_patch(
            None,
            {"themes": {"made_up_theme": False}},
            catalog.theme_rows,
        )


def test_content_preferences_reject_retired_vulgarity_setting():
    catalog = ContentCatalog.load()

    with pytest.raises(ContentError, match="unknown preference fields"):
        merge_preference_patch(
            None,
            {"max_vulgarity": "normal"},
            catalog.theme_rows,
        )
