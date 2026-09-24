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

    assert metadata == mini_assets


def test_round_complete_pack_is_available():
    catalog = ContentCatalog.load()
    choices = catalog.eligible_mascots("round.end.scramble.complete")
    assert choices
    assert all(
        "round.end.scramble.complete" in row["events"]
        for row in choices
    )


def test_score_reports_have_score_specific_banter_without_needing_minis():
    catalog = ContentCatalog.load()
    banter = catalog.eligible_banter("score.report.individual.birdie")
    assert banter
    assert all(
        "score.report.individual.birdie" in row["events"]
        or "score.report.scramble.birdie" in row["events"]
        for row in banter
    )


def test_score_response_random_has_its_own_trash_talk_bank():
    catalog = ContentCatalog.load()
    banter = catalog.eligible_banter("score.response.random")
    assert banter
    assert all("score.response.random" in row["events"] for row in banter)


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


def test_existing_mascot_audit_summary_tracks_all_assets():
    catalog = ContentCatalog.load()
    summary = catalog.mascot_audit_summary()

    assert summary["pending"] + summary["verified"] == len(catalog.mascots)
    assert all("copy" in row for row in catalog.mascots)
    assert all("hat_copy" in row for row in catalog.mascots)
    assert all("notes" in row for row in catalog.mascots)


def test_strict_mascot_audit_requires_verified_metadata():
    catalog = ContentCatalog.load()

    # The committed catalog may legitimately be fully audited.
    catalog.validate(strict_mascot_audit=True)

    original_status = catalog.mascots[0]["audit_status"]
    catalog.mascots[0]["audit_status"] = "pending"
    try:
        try:
            catalog.validate(strict_mascot_audit=True)
        except Exception as error:
            assert "has not been visually audited" in str(error)
        else:
            raise AssertionError(
                "strict audit validation should reject pending mascot metadata"
            )
    finally:
        catalog.mascots[0]["audit_status"] = original_status


def test_signin_idle_has_approved_heckle_bank():
    catalog = ContentCatalog.load()
    catalog.validate()

    rows = catalog.eligible_banter(
        "auth.signin.idle",
        max_vulgarity="brutal",
    )
    assert len(rows) == 46
    assert all(row["events"] == ["auth.signin.idle"] for row in rows)
    assert all(row.get("enabled", True) for row in rows)
    assert any("FUCKING PUTT" in row["text"] for row in rows)
    assert any("DELICATE FLOWER" in row["text"] for row in rows)


def test_approved_screen_copy_pools_are_persisted():
    catalog = ContentCatalog.load()
    catalog.validate()

    expected = {
        "auth.signin.idle": 46,
        "auth.create_account.idle": 28,
        "auth.recover.idle": 30,
        "auth.login_failed": 27,
        "auth.account_created": 29,
        "auth.recovery_key_warning": 23,
        "auth.password_changed": 30,
        "auth.logout": 24,
        "auth.welcome": 29,
        "auth.create_account_failed": 20,
        "auth.recovery_failed": 21,
        "auth.password_changed.recovery": 10,
        "auth.username_taken": 19,
        "auth.password_invalid": 14,
        "auth.username_invalid": 20,
        "auth.display_name_invalid": 20,
        "auth.session_expired": 17,
        "auth.recovery_key_issued": 18,
        "auth.recovery_key_invalid_format": 15,
        "auth.system_error": 10,
        "auth.offline": 14,
        "onboarding.install.idle": 20,
        "home.idle": 74,
        "round_setup.idle": 39,
    }

    for event_key, count in expected.items():
        rows = [
            row
            for row in catalog.banter
            if event_key in row.get("events", [])
        ]
        assert len(rows) == count, event_key

    assert all(
        row["vulgarity"] == "normal"
        for row in catalog.banter
        if "auth.signin.idle" in row.get("events", [])
    )

    home_brutal = [
        row
        for row in catalog.banter
        if "home.idle" in row.get("events", [])
        and row["vulgarity"] == "brutal"
    ]
    setup_brutal = [
        row
        for row in catalog.banter
        if "round_setup.idle" in row.get("events", [])
        and row["vulgarity"] == "brutal"
    ]
    assert len(home_brutal) == 18
    assert len(setup_brutal) == 19
    assert all(row.get("themes") for row in home_brutal)
    assert all(row.get("themes") for row in setup_brutal)


def test_default_signed_in_vulgarity_is_brutal():
    from who_pushed_me.content.preferences import public_preferences

    catalog = ContentCatalog.load()
    preferences = public_preferences(None, catalog.theme_rows)
    assert preferences["max_vulgarity"] == "brutal"
