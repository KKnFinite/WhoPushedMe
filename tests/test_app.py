from app import create_app


def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_home_loads_pwa_shell():
    response = client().get("/")
    assert response.status_code == 200
    assert b"WPM_Splash_Login.webp" in response.data
    assert b"START A ROUND" in response.data
    assert b"WPM_Home_Hero_BrightDay.webp" in response.data
    assert b'id="home-hero-art"' in response.data
    assert b"LET\xe2\x80\x99S MAKE A MESS." in response.data
    assert b"ENABLE THE DAMAGE." in response.data
    assert b"PREVIOUS" in response.data and b"DISASTERS" in response.data
    assert b"ALLEGED" in response.data and b"TALENT" in response.data
    assert b"KNOWN" in response.data and b"OFFENDERS" in response.data
    assert b"TAKE 10 SECONDS. MAKE IT AN ACTUAL APP." in response.data
    assert b"FINE. INSTALL THE DAMN THING." in response.data
    assert b"I ENJOY MAKING THINGS HARDER." in response.data
    assert b"APP UNDER CONSTRUCTION, DUMBASS." in response.data
    assert b"SIGN IN" in response.data
    assert b'id="auth-heckle"' in response.data
    assert b"CREATE ACCOUNT" in response.data
    assert b"RECOVER" in response.data
    assert b"SETTINGS" in response.data
    assert b"EVERY ASSHOLE FOR THEMSELVES" in response.data
    assert b"GROSS ONLY" in response.data
    assert b"GROSS + NET" in response.data
    assert b"ROUND HANDICAPS" in response.data
    assert b"HANDICAP INDEX" in response.data
    assert b"WE SUCK TOGETHER" in response.data
    assert b"STARTING HOLE" in response.data
    assert b"APP STARTS COUNTING AT" in response.data
    assert b"LEAVE IT UNTRACKED" in response.data
    assert b"ENTER THE DAMAGE SO FAR" in response.data
    assert b"ENTER PARS NOW" in response.data
    assert b"ENTER AS WE GO" in response.data
    assert b"DON'T TRACK PAR" in response.data
    assert b"PHYSICAL COURSE" in response.data
    assert b"FIND A COURSE" in response.data
    assert b"FREE PLAY" in response.data
    assert b"YOUR TEE" in response.data
    assert b"START THE SHITSHOW" in response.data
    assert b"ROUND BANTER" in response.data
    assert b"NOT A PLACE FOR SNOWFLAKES" in response.data
    assert b"NEXT HOLE" in response.data
    assert b"GO ANYWAY" in response.data
    assert b"ROUND SETTINGS" in response.data
    assert b"SAVE TEE CORRECTION" in response.data
    assert b"JOIN THE ROUND" in response.data
    assert b"ALREADY BEEN PLAYING?" in response.data
    assert b"ENTER THE DAMAGE SO FAR" in response.data
    assert b"NOPE. START HERE." in response.data
    assert b"ARE YOU ALREADY IN THIS MESS?" in response.data
    assert b"ADD OFFLINE GOLFER" in response.data
    assert b"END ROUND EARLY" in response.data
    assert b"FINE. I'LL PLAY." in response.data
    assert b"BACK TO LIVE" in response.data
    assert b"SET PAR" in response.data
    assert b"Talk your shit..." in response.data
    assert b"BAG OF BULLSHIT" in response.data
    assert b"THROW IN THE TOWEL" in response.data
    assert b"YEP. I'M DONE." in response.data
    assert b"CALL SOMEONE OUT" in response.data
    assert b"NICE FUCKING SHOT" in response.data
    assert b"CALL YOUR SHOT" in response.data
    assert b"YOU WON'T" in response.data
    assert b"EXCUSE DEPARTMENT" in response.data
    assert b"OPEN MIC" in response.data
    assert b"SCRAMBLE CONTRIBUTIONS" in response.data
    assert b"FINISH THE DISASTER" in response.data
    assert b"FIX THE SCORECARD" in response.data
    assert b"FINISH INCOMPLETE" in response.data
    assert b"ROUND OVER" in response.data
    assert b"RECEIPTS" in response.data
    assert b"DOWNLOAD FINAL DAMAGE REPORT (PDF)" in response.data
    assert b"MINI MASCOTS" in response.data
    assert b"TRASH TALK" in response.data
    assert b"DRINKING JOKES" in response.data
    assert b"WIFE JOKES" in response.data
    assert b"VULGARITY" not in response.data
    assert b'max_vulgarity' not in response.data
    assert b"manifest.webmanifest" in response.data


def test_health():
    response = client().get("/health")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["status"] == "ok"
    assert payload["service"] == "who-pushed-me-scorecard"
    assert payload["version"] == "0.3.0"


def test_old_round_routes_are_parked():
    get_response = client().get("/new-round")
    post_response = client().post("/round-preview")
    assert get_response.status_code == 302
    assert post_response.status_code == 302
    assert get_response.headers["Location"].endswith("/")
    assert post_response.headers["Location"].endswith("/")


def test_service_worker_is_served_from_root_scope():
    response = client().get("/service-worker.js")
    assert response.status_code == 200
    assert b"wpm-shell-v87" in response.data
    assert response.headers["Cache-Control"] == "no-cache"


def test_critical_frontend_assets_are_versioned_and_network_first():
    page = client().get("/")
    assert page.status_code == 200
    assert b"/static/app.css?v=0.3.0" in page.data
    assert b"/static/app.js?v=0.3.0" in page.data

    worker = client().get("/service-worker.js")
    assert worker.status_code == 200
    assert b"CRITICAL_FRONTEND_PATHS" in worker.data
    assert b"fetch(event.request, { cache: 'no-store' })" in worker.data


def test_join_round_uses_approved_dedicated_mock_pool():
    page = client().get("/")
    assert page.status_code == 200
    assert b'id="join-round-heckle"' in page.data
    assert b'id="join-round-heckle-text"' in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"'roundJoin'" in script.data
    assert b"'round_join.idle'" in script.data

    from who_pushed_me.content.catalog import ContentCatalog

    catalog = ContentCatalog.load()
    rows = catalog.eligible_banter("round_join.idle")
    assert len(rows) == 32
    texts = {row["text"] for row in rows}
    assert "TYPE THE 4 DIGITS. IT’S NOT THE FUCKING DA VINCI CODE." in texts
    assert "PUT IN THE CODE, TECHNOLOGY HERCULES." not in texts
    assert "IF YOU NEED HELP WITH FOUR DIGITS, STAY OUT OF THE SCORECARD." not in texts
    assert "FOUR DIGITS STANDING BETWEEN YOU AND EMBARRASSING YOURSELF ON PURPOSE." not in texts


def test_mobile_focus_does_not_zoom_the_layout():
    page = client().get("/")
    assert page.status_code == 200
    assert b"width=device-width" in page.data
    assert b"initial-scale=1" in page.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"IOS FOCUS ZOOM HARD LOCK" in css.data
    assert b"touch-action: manipulation" in css.data
    assert b"font-size: 17px !important" in css.data
    assert b'[contenteditable="true"]' in css.data
    assert b".live-score-input" in css.data
    assert b"font-size: 1.75rem !important" in css.data


def test_asset_builder_keeps_shell_cache_version_in_sync():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    builder = (root / "tools" / "build_assets.py").read_text(encoding="utf-8")
    assert "wpm-shell-v87" in builder
    assert "/static/assets/_meta/asset-manifest.json" in builder


def test_launch_splash_uses_approved_art_for_three_seconds_then_login_overlay():
    response = client().get("/")
    assert response.status_code == 200
    assert b'class="splash-art"' in response.data
    assert b"WPM_Splash_Login.webp" in response.data
    assert b'id="launch-splash-mini"' not in response.data

    asset = client().get("/static/assets/brand/WPM_Splash_Login.webp")
    assert asset.status_code == 200
    assert asset.data[:4] == b"RIFF"
    assert asset.data[8:12] == b"WEBP"

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"window.setTimeout(revealShell, 3000)" in script.data
    assert b"splash.classList.add('splash-auth-ready')" in script.data


def test_live_scorecard_exposes_score_removal_control():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"REMOVE SCORE" in response.data
    assert b"method: 'DELETE'" in response.data


def test_live_scorecard_uses_unique_reaction_and_challenge_controls():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"CHALLENGE SCORE" in response.data
    assert b"UPDATE CHALLENGE" in response.data
    assert b"/reaction" in response.data
    assert b"talk_shit" in response.data

def test_lobby_is_social_and_tee_choice_happens_before_entry():
    page = client().get("/")
    assert page.status_code == 200
    assert b'id="join-tee-field"' in page.data
    assert b'id="lobby-banter-feed"' in page.data
    assert b'id="lobby-banter-form"' in page.data
    assert b'id="lobby-tee-panel"' not in page.data
    assert b'id="lobby-handicap-panel"' not in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"LOBBY_BANTER_ROTATE_MS = 10000" in script.data
    assert b"lobby.idle" in script.data
    assert b"prepareJoinTeeChoice" in script.data
    assert b"tee_name: teeName || null" in script.data
    assert b"lobbyBanterForm?.addEventListener" in script.data


def test_lobby_idle_banter_is_registered_and_admin_editable():
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    events = json.loads(
        (root / "who_pushed_me" / "content" / "events.json").read_text(
            encoding="utf-8"
        )
    )
    banter = json.loads(
        (root / "who_pushed_me" / "content" / "banter.json").read_text(
            encoding="utf-8"
        )
    )
    admin = (root / "tools" / "content_admin.py").read_text(encoding="utf-8")

    lobby_idle = next(
        row for row in events["events"] if row["key"] == "lobby.idle"
    )
    assert lobby_idle["triggerable"] is True
    assert lobby_idle["admin_toggleable"] is True

    lobby_rows = [
        row for row in banter["banter"]
        if "lobby.idle" in row.get("events", [])
    ]
    assert len(lobby_rows) >= 12
    assert '"lobby.idle": 160' in admin



def test_receipts_keep_score_social_history_visible():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"REACTIONS:" in response.data
    assert b"CHALLENGES:" in response.data


def test_install_onboarding_uses_approved_mascot_assets():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"WPM_Onboarding_Install_StopOpeningThisLikeAPsychopath.webp" in response.data
    assert b"WPM_Onboarding_Install_LiterallyTellingYouWhereToTap.webp" in response.data
    assert b"WPM_Onboarding_Install_PutMeOnYourFuckingHomeScreen.webp" in response.data
    assert b"WPM_Onboarding_Install_MakeItAnAppYouLazyBastard.webp" in response.data
    assert b"WPM_Onboarding_Install_47OtherUselessApps.webp" in response.data


def test_round_setup_sends_route_and_par_tracking_choices():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"start_hole: startHole" in response.data
    assert b"par_tracking_enabled: parSetup !== 'off'" in response.data
    assert b"course_hole_count" in response.data
    assert b"Saving pars..." in response.data


def test_live_spectator_can_promote_into_play():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"/join-play" in response.data
    assert b"Pick a tee before joining the round." in response.data


def test_scramble_uses_one_shared_team_tee():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"scramble_tee_name" in response.data
    assert b"TEAM SCORING TEE" in response.data
    assert b"TEAM TEE:" in response.data
    assert b"Pick one team scoring tee before the round starts." in response.data


def test_scramble_team_tee_migration_is_present():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    migration = (
        root / "migrations" / "0010_scramble_team_tee.sql"
    ).read_text(encoding="utf-8")
    assert "ADD COLUMN scramble_tee_name" in migration
    assert "r.mode = 'scramble'" in migration


def test_manual_next_hole_warns_but_can_go_anyway():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"missingScoresAtPosition" in response.data
    assert b"YOU CAN FIX IT NOW OR MOVE ON WITHOUT INVENTING A SCORE." in response.data
    assert b"advanceWarningGo" in response.data


def test_live_round_settings_exposes_tee_correction():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"round-settings-tee-select" in response.data
    assert b"/tee" in response.data
    assert b"TEAM SCORING TEE" in response.data


def test_bag_does_not_offer_generic_reaction_strip():
    response = client().get("/")
    assert response.status_code == 200
    assert b'data-reaction=' not in response.data


def test_missing_par_blocks_score_then_resumes_after_par_entry():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"pendingScoreAfterPar" in response.data
    assert b"WE NEED PAR BEFORE WE CAN JUDGE YOU PROPERLY." in response.data
    assert b"player_participant_id = pending.participantId" in response.data


def test_backfilled_scores_use_compact_summary_instead_of_old_popup_replay():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"JUST FILED" in response.data
    assert b"AFTER THE FACT." in response.data
    assert b"THE HISTORICAL RECORD HAS BEEN CONVENIENTLY UPDATED." in response.data


def test_join_flow_checks_round_only_golfers_before_new_player():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"/claimable-players" in response.data
    assert b"THAT'S ME" in response.data
    assert b"/claim-player" in response.data


def test_live_round_can_add_offline_golfer_proxy():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"/round-only-players" in response.data
    assert b"Give the offline golfer a name first." in response.data
    assert b"OFFLINE" in response.data


def test_end_early_vote_uses_connected_eligible_players():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"/end-early-vote" in response.data
    assert b"CONNECTED GOLFER" in response.data
    assert b"NO. KEEP SUFFERING." in client().get("/").data


def test_end_early_vote_migration_is_present():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    migration = (
        root / "migrations" / "0011_end_early_votes.sql"
    ).read_text(encoding="utf-8")
    assert "CREATE TABLE round_end_early_votes" in migration
    assert "PRIMARY KEY (round_id, participant_id)" in migration


def test_claim_undo_warns_before_detaching_account_history():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"claimUndoConfirmPending" in response.data
    assert b"THOSE RECEIPTS STAY ATTRIBUTED TO YOUR ACCOUNT." in response.data
    assert b"/claim-player/undo" in response.data


def test_receipts_prefer_actor_identity_snapshot():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"actor_display_name" in response.data


def test_forms_capture_values_before_busy_state():
    response = client().get("/static/app.js")
    source = response.data.decode("utf-8")

    for form_name in (
        "loginForm",
        "registerForm",
        "recoverForm",
        "startRoundForm",
        "joinRoundForm",
    ):
        marker = f"{form_name}?.addEventListener('submit'"
        start = source.index(marker)
        end = source.index("\n  });", start) + len("\n  });")
        block = source[start:end]
        assert block.index(f"new FormData({form_name})") < block.index(
            f"setFormBusy({form_name}, true)"
        )


def test_form_busy_restores_prior_disabled_state():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"const formBusyState = new WeakMap();" in response.data
    assert b"control.disabled = previous?.get(control) ?? false;" in response.data


def test_install_onboarding_listeners_are_bound_once():
    response = client().get("/static/app.js")
    source = response.data.decode("utf-8")

    assert source.count("window.addEventListener('beforeinstallprompt'") == 1
    assert source.count("window.addEventListener('appinstalled'") == 1
    assert source.count("installOnboardingPrimary?.addEventListener('click'") == 1
    assert source.count("installOnboardingSkip?.addEventListener('click'") == 1

    switch_start = source.index("const switchAuthView = (view) => {")
    switch_end = source.index("\n  };", switch_start)
    switch_block = source[switch_start:switch_end]
    assert "beforeinstallprompt" not in switch_block
    assert "installOnboardingPrimary?.addEventListener" not in switch_block


def test_settings_values_are_snapshotted_before_busy_state():
    response = client().get("/static/app.js")
    source = response.data.decode("utf-8")
    start = source.index("settingsForm?.addEventListener('submit'")
    end = source.index("\n  });", start) + len("\n  });")
    block = source[start:end]

    assert block.index("const patch = {") < block.index(
        "setFormBusy(settingsForm, true)"
    )
    assert "body: patch" in block



def test_round_setup_sends_tracking_start_and_prior_hole_mode():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"tracking_start_position: trackingStart" in response.data
    assert b"prior_holes_mode: priorMode" in response.data
    assert b"APP JOINS AT" in response.data


def test_untracked_prior_holes_are_read_only_and_not_par_required():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"route?.state !== 'skipped'" in response.data
    assert b"UNTRACKED HOLE" in response.data
    assert b"This hole was deliberately left untracked." in response.data
    assert b"const plannedRoute = (round.route || []).filter" in response.data



def test_individual_round_setup_can_enable_optional_net_scoring():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"net_scoring_enabled:" in response.data
    assert b"individualScoring === 'net'" in response.data
    assert b"individualScoringFieldset.hidden = mode === 'scramble'" in response.data


def test_round_handicap_editor_allows_manual_fallback_and_confirmed_correction():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"/handicap" in response.data
    assert b"MANUAL ROUND HANDICAP" in response.data
    assert b"NET PLACEMENT PENDING" in response.data
    assert b"CONFIRM CORRECTION" in response.data
    assert b"confirm_correction:" in response.data


def test_net_results_never_show_official_rank_without_official_net_state():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"round.results?.net_official" in response.data
    assert b"NET PENDING HANDICAP" in response.data
    assert b"NET PLACEMENT PENDING" in response.data
    assert b"GROSS + NET OFFICIAL" in response.data


def test_settings_support_optional_profile_handicap_without_ghin():
    response = client().get("/static/app.js")
    shell = client().get("/")
    assert response.status_code == 200
    assert b"/api/profile/handicap" in response.data
    assert b"Handicap Index must be between -10.0 and 54.0." in response.data
    assert b"No GHIN required." in shell.data


def test_net_handicap_migration_is_present():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    migration = (
        root / "migrations" / "0012_net_handicap_foundation.sql"
    ).read_text(encoding="utf-8")
    assert "ADD COLUMN handicap_index" in migration
    assert "ADD COLUMN net_scoring_enabled" in migration
    assert "CREATE TABLE cached_course_tee_ratings" in migration


def test_par_tracking_mode_locks_after_first_score_in_ui():
    response = client().get("/static/app.js")
    shell = client().get("/")
    assert response.status_code == 200
    assert b"/par-tracking" in response.data
    assert b"LOCKED AFTER FIRST FACTUAL SCORE." in response.data
    assert b"(round.scores || []).length > 0" in response.data
    assert b"TRACK PAR" in shell.data
    assert b"DON'T TRACK PAR" in shell.data


def test_receipts_show_personal_unread_catchup_badge():
    shell = client().get("/")
    script = client().get("/static/app.js")
    assert shell.status_code == 200
    assert script.status_code == 200
    assert b"YOU MISSED SOME SHIT" in shell.data
    assert b"receipts_state?.unseen_count" in script.data
    assert b"/receipts-seen" in script.data
    assert b"receiptMarkInFlight" in script.data


def test_receipt_seen_state_migration_is_present():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    migration = (
        root / "migrations" / "0013_receipt_seen_state.sql"
    ).read_text(encoding="utf-8")
    assert "CREATE TABLE round_receipt_seen_state" in migration
    assert "last_seen_event_id" in migration
    assert "PRIMARY KEY (participant_id)" in migration


def test_late_joiner_gets_explicit_backfill_path_without_requiring_old_scores():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"earlierBackfillable" in response.data
    assert b"viewer?.tracked_from_position" in response.data
    assert b"route.state !== 'skipped'" in response.data
    assert b"BACKFILLING OLD DAMAGE. USE BACK TO LIVE WHEN YOU ARE DONE." in response.data
    assert b"wpm_late_backfill_dismissed:" in response.data


def test_backfill_summary_stays_compact_instead_of_replaying_old_popups():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"item.data?.backfilled" in response.data
    assert b"JUST FILED" in response.data
    assert b"THE HISTORICAL RECORD HAS BEEN CONVENIENTLY UPDATED." in response.data


def test_ui_phase_uses_full_screen_mobile_round_surface():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    css = (root / "static" / "app.css").read_text(encoding="utf-8")
    assert "UI PHASE 1: MOBILE-FIRST GAME SURFACE" in css
    assert "@media (max-width: 680px)" in css
    assert "height: 100dvh;" in css
    assert "position: sticky;" in css
    assert "grid-template-columns: minmax(0, 1fr) 104px;" in css


def test_ui_direction_document_is_present():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    direction = (root / "docs" / "ui-direction.md").read_text(encoding="utf-8")
    assert "multiplayer golf game with a social feed" in direction
    assert "Mobile is the primary layout." in direction


def test_official_wpm_palette_and_safe_area_branding():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"--wpm-night: #050907" in css.data
    assert b"--wpm-green-deep: #173326" in css.data
    assert b"--wpm-green: #214534" in css.data
    assert b"--wpm-green-moss: #355b45" in css.data
    assert b"--wpm-green-accent: #4e7a5d" in css.data
    assert b"--wpm-orange-burnt: #d96d3b" in css.data
    assert b"--wpm-orange-ember: #e9783e" in css.data
    assert b"--wpm-orange-danger: #f25c1d" in css.data
    assert b"--wpm-gold: #d4a62a" in css.data
    assert b'--font-wpm-light: "WPM Sans"' in css.data
    assert b'--font-wpm-regular: "WPM Sans"' in css.data
    assert b'--font-wpm-bold: "WPM Sans"' in css.data

    manifest = client().get("/static/manifest.webmanifest")
    assert manifest.status_code == 200
    payload = manifest.get_json()
    assert payload["background_color"] == "#050907"
    assert payload["theme_color"] == "#050907"

    home = client().get("/")
    assert b'<meta name="theme-color" content="#050907">' in home.data


def test_signin_idle_heckle_rotation_uses_content_bank():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"/api/content/messages" in response.data
    assert b"auth.signin.idle" in response.data
    assert b"AUTH_HECKLE_ROTATE_MS = 5000" in response.data
    assert b"AUTH_HECKLE_RESUME_MS = 9000" in response.data
    assert b"pauseAuthHecklesForInteraction" in response.data
    assert b"refillAuthHeckleBag" in response.data


def test_asset_builder_keeps_approved_splash_in_shell_cache():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    builder = (root / "tools" / "build_assets.py").read_text(encoding="utf-8")
    assert "/static/assets/brand/WPM_Splash_Login.webp" in builder


def test_auth_form_uses_locked_wpm_account_rules():
    response = client().get("/")
    assert response.status_code == 200
    assert b'name="display_name" autocomplete="name" maxlength="20"' in response.data
    assert b'name="username" autocomplete="username" minlength="3" maxlength="16"' in response.data
    assert b'name="password" type="password" autocomplete="new-password" minlength="10"' in response.data
    assert b'placeholder="XXXX-XXXX"' in response.data
    assert b'name="new_password" type="password" autocomplete="new-password" minlength="10"' in response.data


def test_auth_and_idle_message_pools_are_wired_into_ui():
    js = client().get("/static/app.js")
    assert js.status_code == 200
    assert b"auth.create_account.idle" in js.data
    assert b"auth.recover.idle" in js.data
    assert b"auth.login_failed" in js.data
    assert b"auth.username_taken" in js.data
    assert b"auth.password_invalid" in js.data
    assert b"auth.recovery_failed" in js.data
    assert b"auth.system_error" in js.data
    assert b"auth.offline" in js.data
    assert b"home.idle" in js.data
    assert b"round_setup.idle" in js.data
    assert b"onboarding.install.idle" in js.data
    assert b"/api/content/messages/user" in js.data


def test_account_forms_use_custom_validation_and_show_rules():
    response = client().get("/")
    assert response.status_code == 200
    assert b'data-auth-panel="register" hidden novalidate' in response.data
    assert b"10 characters minimum" in response.data
    assert b"3\xe2\x80\x9316 characters" in response.data
    assert b"Current keys look like XXXX-XXXX" in response.data
    assert b'id="recovery-key-snark"' in response.data
    assert b'id="home-heckle"' in response.data
    assert b'id="round-setup-heckle"' in response.data


def test_hidden_splash_cannot_override_main_app_on_ios():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b".launch-splash[hidden]" in css.data
    assert b"display: none !important;" in css.data


def test_home_hero_pool_and_layers_are_wired():
    import json

    page = client().get("/")
    assert page.status_code == 200
    assert b'class="home-hero"' in page.data
    assert b'id="home-hero-art"' in page.data
    assert b'id="home-welcome-name"' in page.data
    assert b'data-settings-open' in page.data
    assert b'id="home-heckle"' in page.data
    assert b"home-wordmark" not in page.data
    assert b"home-mascot" not in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"home.heroes" in script.data
    assert b"HOME_HERO_SESSION_KEY" in script.data
    assert b"homeHeroArt.src" in script.data
    assert b"home.backgrounds" not in script.data

    manifest_response = client().get("/static/assets/_meta/asset-manifest.json")
    assert manifest_response.status_code == 200
    manifest = json.loads(manifest_response.data)
    heroes = [
        item for item in manifest["assets"]
        if item.get("pool") == "home.heroes" and item.get("enabled", True)
    ]
    assert manifest["home_hero_count"] == 5
    assert len(heroes) == 5
    assert all(item["production"].endswith(".webp") for item in heroes)

    default_hero = client().get(
        "/static/assets/home/heroes/WPM_Home_Hero_BrightDay.webp"
    )
    assert default_hero.status_code == 200
    assert default_hero.data[:4] == b"RIFF"
    assert default_hero.data[8:12] == b"WEBP"


def test_home_art_is_precached_for_installed_pwa():
    worker = client().get("/service-worker.js")
    assert worker.status_code == 200
    assert b"WPM_Home_Hero_BrightDay.webp" in worker.data
    assert b"WPM_Home_Hero_CreekBridge.webp" in worker.data
    assert b"WPM_Home_Hero_GoldenHour.webp" in worker.data
    assert b"WPM_Home_Hero_StormySunset.webp" in worker.data
    assert b"WPM_Home_Hero_SunriseCourse.webp" in worker.data
    assert b"WPM_Home_Mascot.png" not in worker.data
    assert b"WPM_Home_Background_SunriseBridge.webp" not in worker.data


def test_content_admin_supports_home_background_pool():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    admin = (root / "tools" / "content_admin.py").read_text(encoding="utf-8")
    builder = (root / "tools" / "build_assets.py").read_text(encoding="utf-8")

    assert "list-home-backgrounds" in admin
    assert "add-home-background" in admin
    assert "remove-home-background" in admin
    assert "home.backgrounds" in admin
    assert 'source.suffix.lower() == ".webp"' in admin
    assert "HOME_BACKGROUNDS_SRC" in builder
    assert "(copied exact source)" in builder


def test_content_admin_supports_home_hero_pool():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    admin = (root / "tools" / "content_admin.py").read_text(encoding="utf-8")
    builder = (root / "tools" / "build_assets.py").read_text(encoding="utf-8")

    assert "list-home-heroes" in admin
    assert "add-home-hero" in admin
    assert "remove-home-hero" in admin
    assert "home.heroes" in admin
    assert "HOME_HERO_SRC" in admin
    assert "HOME_HEROES_SRC" in builder
    assert "build_home_hero_webps" in builder
    assert '"home_hero_count": home_hero_count' in builder


def test_home_hero_preserves_full_portrait_art_without_crop():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"aspect-ratio: 941 / 1672" in css.data
    assert b"object-fit: contain" in css.data


def test_home_buttons_use_legible_temporary_ui_fonts():
    page = client().get("/")
    assert page.status_code == 200
    assert b"Bebas+Neue" in page.data
    assert b"Barlow+Condensed" in page.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b'font-family: "Bebas Neue"' in css.data
    assert b'font-family: "Barlow Condensed"' in css.data
    assert b"HOME LEGIBILITY PASS" in css.data


def test_home_is_single_screen_without_secondary_button_clutter():
    page = client().get("/")
    assert page.status_code == 200
    assert b"RERUN THE DAMAGE." not in page.data
    assert b"SEE THE LIES." not in page.data
    assert b"SAME SUSPECTS." not in page.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"HOME NO-SCROLL COMPACT LAYOUT" in css.data
    assert b"height: 100dvh" in css.data
    assert b"overflow: hidden" in css.data
    assert b"position: absolute" in css.data
    assert b"bottom: 0" in css.data


def test_home_menu_is_nested_inside_fixed_hero_overlay():
    page = client().get("/")
    assert page.status_code == 200
    html = page.data.decode("utf-8")
    hero_start = html.index('<section class="home-hero"')
    menu_start = html.index('<section class="home-menu"', hero_start)
    hero_end = html.index('</section>', menu_start)
    assert hero_start < menu_start < hero_end

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"HOME OVERLAY FINAL FIX" in css.data
    assert b"position: fixed" in css.data
    assert b"height: 100dvh" in css.data
    assert b"body.app-ready .home-menu" in css.data
    assert b"bottom: 0" in css.data
    assert b"object-fit: cover" in css.data


def test_home_banter_sits_above_buttons_and_hero_respects_safe_area():
    page = client().get("/")
    assert page.status_code == 200
    html = page.data.decode("utf-8")
    menu_start = html.index('<section class="home-menu"')
    banter_start = html.index('id="home-heckle"', menu_start)
    primary_start = html.index('class="home-primary-actions"', menu_start)
    assert menu_start < banter_start < primary_start

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"HOME SAFE-AREA + TOP BANTER TUNE" in css.data
    assert b"--home-art-top-offset" in css.data
    assert b"env(safe-area-inset-top)" in css.data
    assert b"font-size: clamp(.96rem, 3.8vw, 1.12rem)" in css.data


def test_home_hero_keeps_left_logo_margin_on_iphone():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"object-position: 36% top" in css.data


def test_ios_status_bar_is_solid_black():
    page = client().get("/")
    assert page.status_code == 200
    assert b'apple-mobile-web-app-status-bar-style" content="black"' in page.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"IPHONE STATUS BAR COVER" in css.data
    assert b"height: max(44px, env(safe-area-inset-top))" in css.data


def test_android_pwa_uses_black_status_bar_theme():
    import json

    page = client().get("/")
    assert page.status_code == 200
    assert b'<meta name="theme-color" content="#000000">' in page.data

    manifest_response = client().get("/static/manifest.webmanifest")
    assert manifest_response.status_code == 200
    manifest = json.loads(manifest_response.data)
    assert manifest["theme_color"] == "#000000"
    assert manifest["background_color"] == "#000000"


def test_home_banter_text_is_larger():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"MOBILE STATUS BAR COVER" in css.data
    assert b"font-size: clamp(1.04rem, 4.15vw, 1.22rem)" in css.data


def test_start_round_uses_dark_game_setup_surface():
    page = client().get("/")
    assert page.status_code == 200
    assert b'round-flow-card round-flow-card-game' in page.data
    assert b'round-flow-form round-start-form' in page.data
    assert b'setup-card setup-card-mode' in page.data
    assert b'setup-card setup-card-route' in page.data
    assert b'setup-card setup-card-par' in page.data
    assert b'round-create-button' in page.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"ROUND SETUP DARK GAME SURFACE" in css.data
    assert b".round-start-form .choice-fieldset label:has(input:checked)" in css.data
    assert b"position: sticky" in css.data
    assert b"CREATE THE DISASTER" in page.data


def test_start_round_is_fixed_three_step_wizard():
    page = client().get("/")
    assert page.status_code == 200
    assert page.data.count(b'data-setup-step="') == 3
    assert b'data-setup-next="2"' in page.data
    assert b'data-setup-next="3"' in page.data
    assert b'data-setup-back="1"' in page.data
    assert b'data-setup-back="2"' in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"const setSetupStep =" in script.data
    assert b"setupNextButtons.forEach" in script.data
    assert b"results.slice(0, 3)" in script.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"START ROUND FIXED WIZARD" in css.data
    assert b"overflow: hidden" in css.data
    assert b"grid-template-rows: 28px minmax(0, 1fr)" in css.data
    assert b"-webkit-line-clamp: 3" in css.data
    assert b"height: 86px" in css.data


def test_start_round_banner_is_fixed_and_modes_show_real_names():
    page = client().get("/")
    assert page.status_code == 200
    assert b"INDIVIDUAL" in page.data
    assert b"SCRAMBLE" in page.data
    assert b"EVERY ASSHOLE FOR THEMSELVES" in page.data
    assert b"WE SUCK TOGETHER" in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"roundSetupHeckle.hidden = false" in script.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"START ROUND WIZARD STABILITY PASS" in css.data
    assert b"block-size: 88px !important" in css.data
    assert b"min-height: 68px !important" in css.data
    assert b"padding-bottom: 28px" in css.data


def test_round_setup_uses_standard_cards_minis_and_theme_tease():
    page = client().get("/")
    assert page.status_code == 200
    assert b'id="setup-mini-stage"' in page.data
    assert b'id="setup-mini"' in page.data
    assert b'id="color-theme-tease"' in page.data
    assert b"WPM GREEN" in page.data
    assert b"<small>INDIVIDUAL</small>" in page.data
    assert b"<small>SCRAMBLE</small>" in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"const loadRandomSetupMini" in script.data
    assert b"event_key === 'round_start'" in script.data
    assert b"results.slice(0, 2)" in script.data
    assert b"STFU, snowflake" in script.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"ROUND SETUP CONSISTENCY + MINI PASS" in css.data
    assert b".setup-step #prior-holes-mode" in css.data
    assert b".setup-mini-stage" in css.data
    assert b"max-height: 108px" in css.data


def test_start_round_course_precedes_route_and_mini_overlays_next():
    page = client().get("/")
    assert page.status_code == 200
    html = page.data.decode("utf-8")

    step1 = html.index('data-setup-step="1"')
    step2 = html.index('data-setup-step="2"')
    step3 = html.index('data-setup-step="3"')
    course = html.index('setup-card-course-mode', step2)
    route = html.index('setup-card-route', step3)
    par = html.index('setup-card-par', step3)

    assert step1 < step2 < step3
    assert step2 < course < step3
    assert step3 < route < par
    assert b"NEXT: COURSE" in page.data
    assert b"NEXT: ROUTE" in page.data
    assert b"setup-step-actions-with-mini" in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"setCourseStepMessage" in script.data
    assert b"Pick a course first, or switch to Free Play." in script.data
    assert b"target === 3" in script.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"ROUND SETUP FLOW ORDER + MINI OVERLAY" in css.data
    assert b"bottom: 43px" in css.data
    assert b"min-height: 56px !important" in css.data
    assert b"max-height: 104px" in css.data


def test_setup_mini_is_planted_on_visible_next_button():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"STEP 1 MINI PLANTED ON BUTTON" in css.data
    assert b"bottom: 34px !important" in css.data
    assert b"bottom: 84px !important" in css.data
    assert b"height: 52px !important" in css.data


def test_round_setup_message_contract_and_content_limits():
    import pytest

    from tools.content_admin import (
        _banter_max_chars,
        _validate_banter_copy_limits,
    )
    from who_pushed_me.content.catalog import ContentError

    page = client().get("/")
    assert page.status_code == 200
    assert b'id="round-setup-heckle" class="screen-heckle screen-heckle-compact">' in page.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"ROUND SETUP FIXED ACTIONS + MESSAGE CONTRACT" in css.data
    assert b"block-size: 120px !important" in css.data
    assert b"-webkit-line-clamp: 4 !important" in css.data
    assert b"bottom: max(14px, env(safe-area-inset-bottom)) !important" in css.data
    assert b"max-height: 154px !important" in css.data

    assert _banter_max_chars(["round_setup.idle"]) == 160
    assert _banter_max_chars(["home.idle"]) == 320
    assert _banter_max_chars(["some.future.fixed.surface"]) == 160
    assert _banter_max_chars(["home.idle", "round_setup.idle"]) == 160

    _validate_banter_copy_limits([
        {"id": "ok", "text": "x" * 160, "events": ["round_setup.idle"]},
        {"id": "home-ok", "text": "x" * 320, "events": ["home.idle"]},
    ])
    with pytest.raises(ContentError):
        _validate_banter_copy_limits([
            {"id": "too-long", "text": "x" * 161, "events": ["round_setup.idle"]},
        ])


def test_setup_actions_are_locked_to_mobile_viewport():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"ROUND SETUP VIEWPORT-LOCKED ACTION BAR" in css.data
    assert b"position: fixed !important" in css.data
    assert b"bottom: max(12px, env(safe-area-inset-bottom)) !important" in css.data
    assert b"bottom: calc(max(12px, env(safe-area-inset-bottom)) + 48px) !important" in css.data


def test_individual_scoring_uses_golf_terms_and_helpers():
    page = client().get("/")
    assert page.status_code == 200
    assert b"STROKE PLAY SCORING" in page.data
    assert b"GROSS STROKE PLAY" in page.data
    assert b"NET STROKE PLAY" in page.data
    assert b"Every stroke counts. No handicap alibi." in page.data
    assert b"Gross still counts. Handicap math adds net standings." in page.data
    assert b"Missing handicaps never block play." not in page.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"REAL GOLF SCORING COPY" in css.data
    assert b".setup-scoring-option .setup-option-copy" in css.data


def test_setup_steps_two_and_three_match_step_one_actions_and_minis():
    page = client().get("/")
    assert page.status_code == 200
    assert page.data.count(b'data-setup-mini-stage="') == 3
    assert page.data.count(b'data-setup-mini="') == 3

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"results.slice(0, 3)" in script.data
    assert b"loadRandomSetupMini(resolved)" in script.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"UNIFIED SETUP ACTIONS + THREE COURSE RESULTS" in css.data
    assert b"width: 80% !important" in css.data
    assert b"max-height: 158px !important" in css.data


def test_setup_back_and_primary_share_page_one_total_width():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"SETUP BACK + PRIMARY SAME TOTAL WIDTH" in css.data
    assert b"width: 80% !important" in css.data
    assert b"grid-template-columns: 28% minmax(0, 1fr) !important" in css.data
    assert b"width: 84% !important" in css.data


def test_setup_paired_actions_and_free_play_card_are_consistent():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"FINAL SETUP ACTION ROW + FREE PLAY CARD FIX" in css.data
    assert b"grid-template-columns: 30% minmax(0, 1fr) !important" in css.data
    assert b"width: 80% !important" in css.data
    assert b"bottom: calc(max(12px, env(safe-area-inset-bottom)) + 58px) !important" in css.data
    assert b".setup-card-free-play .compact-choice-fieldset" in css.data
    assert b"rgba(18,29,22,.97)" in css.data


def test_free_play_hides_course_panel_and_step_two_mini():
    page = client().get("/")
    assert page.status_code == 200
    assert b"SELECT HOLES" in page.data
    assert b"PHYSICAL COURSE" not in page.data
    assert b"Looping the same nine twice? Pick 9 here and 18 for the round." in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"stepTwoMiniStage.hidden = !useCourse" in script.data
    assert b"freePlaySelected" in script.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"FREE PLAY + STEP 2/3 ACTION FINAL OVERRIDE" in css.data
    assert b"#course-search-panel[hidden]" in css.data
    assert b"#free-play-field[hidden]" in css.data
    assert b"grid-template-columns: 24% minmax(0, 1fr) !important" in css.data
    assert b"bottom: calc(max(12px, env(safe-area-inset-bottom)) + 50px) !important" in css.data


def test_course_step_owns_round_holes_and_hides_mini_during_results():
    page = client().get("/")
    assert page.status_code == 200
    html = page.data.decode("utf-8")
    assert html.count('name="holes"') == 2
    assert "ROUND HOLES" in html
    assert "course_hole_count" not in html
    assert "SELECT HOLES" not in html

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"syncStepTwoMiniVisibility" in script.data
    assert b"searchResultsVisible" in script.data
    assert b"Course data says 9 holes." in script.data
    assert b"body.course_hole_count = holes" in script.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"COURSE STEP HOLES + MINI FINAL PLACEMENT" in css.data
    assert b'bottom: calc(max(12px, env(safe-area-inset-bottom)) + 46px) !important' in css.data
