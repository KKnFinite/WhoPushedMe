from who_pushed_me.content.catalog import ContentCatalog, EventRegistry


def test_event_registry_aliases_and_lineage():
    registry = EventRegistry.load()
    assert registry.canonical_key("round_end_complete") == "round.end.scramble.complete"
    assert registry.lineage("mid_hole.callout.water_shot")[:3] == [
        "mid_hole.callout.water_shot",
        "mid_hole.callout",
        "mid_hole",
    ]
    assert registry.lineage("mid_hole.callout.water_shot")[-1] == "generic.golf"


def test_existing_minis_have_complete_content_metadata():
    catalog = ContentCatalog.load()
    catalog.validate()

    mini_assets = {
        row["asset_id"]
        for row in catalog.asset_manifest["assets"]
        if row.get("family") == "mini-mascot"
    }
    metadata = {row["asset_id"] for row in catalog.mascots}

    assert len(mini_assets) == 97
    assert metadata == mini_assets


def test_round_complete_pack_is_exactly_25():
    catalog = ContentCatalog.load()
    choices = catalog.eligible_mascots("round.end.scramble.complete")
    assert len(choices) == 25


def test_score_push_pack_is_available_to_specific_push_events():
    catalog = ContentCatalog.load()
    choices = catalog.eligible_mascots("score.push.individual.old_hole_raised")
    assert len(choices) == 7
    assert all("score.push" in row["events"] for row in choices)


def test_water_callout_falls_back_to_generic_banter_only():
    catalog = ContentCatalog.load()
    assert catalog.eligible_mascots("mid_hole.callout.water_shot") == []
    banter = catalog.eligible_banter("mid_hole.callout.water_shot")
    assert banter
    assert all(row["events"] == ["generic.golf"] for row in banter)


def test_admin_parent_override_disables_descendants():
    registry = EventRegistry.load()
    assert registry.is_enabled("mid_hole.callout.water_shot")
    assert not registry.is_enabled(
        "mid_hole.callout.water_shot",
        {"mid_hole.callout": False},
    )


def test_theme_registry_is_data_driven():
    catalog = ContentCatalog.load()
    assert {"drinking", "wife"} <= set(catalog.themes)
    assert all("user_toggle" in row for row in catalog.theme_rows)
