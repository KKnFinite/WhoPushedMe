from app import create_app


def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_home_loads_pwa_shell():
    response = client().get("/")
    assert response.status_code == 200
    assert b"IT HAS BEGUN!" in response.data
    assert b"START A ROUND" in response.data
    assert b"TAKE 10 SECONDS. MAKE IT AN ACTUAL APP." in response.data
    assert b"FINE. INSTALL THE DAMN THING." in response.data
    assert b"I ENJOY MAKING THINGS HARDER." in response.data
    assert b"APP UNDER CONSTRUCTION, DUMBASS." in response.data
    assert b"SIGN IN" in response.data
    assert b"CREATE ACCOUNT" in response.data
    assert b"RECOVER" in response.data
    assert b"Settings" in response.data
    assert b"EVERY ASSHOLE FOR THEMSELVES" in response.data
    assert b"WE SUCK TOGETHER" in response.data
    assert b"STARTING HOLE" in response.data
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
    assert b"wpm-shell-v30" in response.data
    assert response.headers["Cache-Control"] == "no-cache"


def test_asset_builder_keeps_shell_cache_version_in_sync():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    builder = (root / "tools" / "build_assets.py").read_text(encoding="utf-8")
    assert "wpm-shell-v30" in builder


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
