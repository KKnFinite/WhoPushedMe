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
    assert b"LIVE SCORECARD" in response.data
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
    assert b"REPORT PAR" in response.data
    assert b"LATEST RECEIPT" in response.data
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
    assert b"BRUTAL" in response.data
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
    assert b"wpm-shell-v49" in response.data
    assert response.headers["Cache-Control"] == "no-cache"


def test_asset_builder_keeps_shell_cache_version_in_sync():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    builder = (root / "tools" / "build_assets.py").read_text(encoding="utf-8")
    assert "wpm-shell-v49" in builder
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
