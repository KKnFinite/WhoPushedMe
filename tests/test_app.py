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


def test_join_round_pins_cta_and_uses_join_mini_pool():
    page = client().get("/")
    assert page.status_code == 200
    assert b'id="join-cta-dock"' in page.data
    assert b'id="join-cta-mini-stage"' in page.data
    assert b'id="join-cta-mini"' in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"loadRandomJoinMini" in script.data
    assert b"player_join_new" in script.data
    assert b"player_join_returning" in script.data
    assert b"player_join_spectator" in script.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"JOIN ROUND BOTTOM CTA + MINI" in css.data
    assert b"position: sticky" in css.data
    assert b".join-cta-dock.has-mini" in css.data


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


def test_incomplete_finish_confirmation_is_not_buried_in_more():
    page = client().get("/")
    assert page.status_code == 200
    html = page.data.decode("utf-8")

    panel = html.index('id="finish-incomplete-panel"')
    footer = html.index('class="live-footer-actions"')
    more = html.index('id="live-more-panel"')

    assert panel < footer
    assert footer < more

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"finishIncompletePanel.scrollIntoView" in script.data


def test_receipts_word_is_removed_from_player_facing_copy():
    page = client().get("/")
    assert page.status_code == 200
    html = page.data.decode("utf-8")

    assert "ROUND HISTORY" in html
    assert "GOLF IS MORE FUN WITH EVIDENCE" in html
    assert "GOLF IS MORE FUN WITH RECEIPTS" not in html

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"THOSE RECEIPTS STAY ATTRIBUTED" not in script.data
    assert b"THAT ROUND HISTORY STAYS ATTRIBUTED" in script.data


def test_final_hole_exposes_finish_round_in_live_footer():
    page = client().get("/")
    assert page.status_code == 200
    html = page.data.decode("utf-8")
    footer_start = html.index('class="live-footer-actions"')
    footer_end = html.index("</div>", footer_start)
    footer = html[footer_start:footer_end]

    assert 'id="advance-live-hole"' in footer
    assert 'id="finish-round-button"' in footer
    assert "FINISH ROUND" in footer

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"canFinishFromFooter" in script.data
    assert b"livePosition === length" in script.data


def test_round_history_never_exposes_internal_event_keys():
    page = client().get("/")
    assert page.status_code == 200
    assert b"ROUND HISTORY" in page.data
    assert b">RECEIPTS<" not in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    source = script.data.decode("utf-8")
    start = source.index("const renderReceipts =")
    end = source.index("const totalParForRound", start)
    history_block = source[start:end]

    assert "pieces.push(event.content_event_key)" not in history_block
    assert "|| event.content_event_key" not in history_block
    assert "|| event.event_type" not in history_block
    assert "ROUND UPDATE" in history_block


def test_round_history_filters_internal_banter_and_shows_factual_score_actions():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const ROUND_HISTORY_EVENT_TYPES =")
    end = source.index("const totalParForRound", start)
    history_block = source[start:end]

    assert "'score_report'" in history_block
    assert "'score_push'" in history_block
    assert "'score_removed'" in history_block
    assert "'par_report'" in history_block
    assert "'par_push'" in history_block
    assert "'score_derived'" not in history_block
    assert "current_hole_auto_advance" not in history_block
    assert "ROUND_HISTORY_EVENT_TYPES.has" in history_block
    assert "roundHistoryTitle(round, event)" in history_block
    assert "STROKES" in history_block



def test_round_history_is_a_dedicated_page_not_inline_or_overlay():
    page = client().get("/")
    assert page.status_code == 200
    html = page.data.decode("utf-8")
    assert 'id="round-history-page"' in html
    assert 'id="round-history-back"' in html
    assert 'data-round-history-open' in html
    assert 'id="receipts-panel"' not in html
    assert "<details" not in html[html.index('id="round-end-panel"'):html.index('id="bag-modal"')]

    css = client().get("/static/app.css")
    assert css.status_code == 200
    source = css.data.decode("utf-8")
    assert "ROUND HISTORY — DEDICATED ROUND PAGE" in source
    assert ".round-history-page > .receipts-list" in source
    assert "overflow-y: auto;" in source
    assert "ROUND HISTORY MOBILE SHEET" not in source
    assert ".receipts-panel[open]" not in source

    script = client().get("/static/app.js")
    assert script.status_code == 200
    js_source = script.data.decode("utf-8")
    assert "const openRoundHistoryPage = () =>" in js_source
    assert "const closeRoundHistoryPage = () =>" in js_source
    assert "liveRoundPanel.hidden = true" in js_source
    assert "roundHistoryPage.hidden = false" in js_source
    assert "roundHistoryBack?.addEventListener('click', closeRoundHistoryPage)" in js_source
    assert "receiptsPanel?.addEventListener('toggle'" not in js_source

def test_round_polling_preserves_open_history_page():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const refreshRound = async (code) =>")
    end = source.index("const refreshLobby = refreshRound", start)
    block = source[start:end]

    assert "roundHistoryPage && !roundHistoryPage.hidden" in block
    assert "currentLobbyRound = round;" in block
    assert "renderReceipts(round);" in block
    assert "return round;" in block
    history_guard = block.index("roundHistoryPage && !roundHistoryPage.hidden")
    normal_render = block.index("renderRoundState(round)")
    assert history_guard < normal_render

def test_score_entry_waits_for_explicit_next_hole():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    store_source = (root / "who_pushed_me" / "store.py").read_text(
        encoding="utf-8"
    )
    start = store_source.index("    def set_score(")
    end = store_source.index("    def remove_score(", start)
    block = store_source[start:end]

    assert "auto_advance = None" in block
    assert "_maybe_advance_active_route(" not in block


def test_join_code_digits_escape_ios_17px_override():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    source = css.data.decode("utf-8")

    assert ":not(.live-score-input):not(.join-code-digit)" in source
    final = source[source.index(
        "/* AUTHORITATIVE JOIN DIGITS + DETACHED LIVE MOMENTS */"
    ):]
    assert "font-size: clamp(4.6rem, 20vw, 5.9rem) !important;" in final
    assert "line-height: .88 !important;" in final


def test_score_announcement_is_outside_live_round_layout():
    page = client().get("/")
    assert page.status_code == 200
    html = page.data.decode("utf-8")

    live_start = html.index('id="live-round-panel"')
    live_end = html.index('id="round-end-panel"', live_start)
    live_block = html[live_start:live_end]
    assert 'id="score-announcement"' not in live_block
    assert html.index('id="score-announcement"') > html.index(
        'id="round-history-page"'
    )


def test_hole_transition_has_continue_and_ten_second_timeout():
    page = client().get("/")
    script = client().get("/static/app.js")
    assert page.status_code == 200
    assert script.status_code == 200

    assert b'id="hole-transition-continue"' in page.data
    assert b"CONTINUE" in page.data

    source = script.data.decode("utf-8")
    assert "dismissHoleTransition" in source
    assert "10000" in source
    assert "holeTransitionContinue?.addEventListener" in source


def test_live_round_has_loud_score_announcement():
    page = client().get("/")
    script = client().get("/static/app.js")
    css = client().get("/static/app.css")
    assert page.status_code == 200
    assert script.status_code == 200
    assert css.status_code == 200

    assert b'id="score-announcement"' in page.data
    assert b'id="score-announcement-text"' in page.data
    assert b"YOU SCORED" in script.data
    assert b"TEAM SCORED" in script.data
    assert b"score_report" in script.data
    assert b"seenScoreAnnouncementEventIds" in script.data
    assert b".score-announcement" in css.data


def test_between_hole_transition_uses_unique_deterministic_mascots():
    page = client().get("/")
    script = client().get("/static/app.js")
    css = client().get("/static/app.css")
    assert page.status_code == 200
    assert script.status_code == 200
    assert css.status_code == 200

    assert b'id="hole-transition"' in page.data
    assert b'id="hole-transition-mascot"' in page.data
    assert b"transitionMascotForPosition" in script.data
    assert b"stableTransitionHash" in script.data
    assert b"scoreSpecificTransitionAssets" in script.data
    assert b"generalTransitionAssets" in script.data
    assert b"used.add(String(picked.asset_id))" in script.data
    assert b"eventKey === 'round_start'" in script.data
    assert b"mascot.full_body.transparent" in script.data
    assert b".hole-transition" in css.data


def test_transition_only_plays_for_new_live_hole():
    script = client().get("/static/app.js")
    assert script.status_code == 200
    source = script.data.decode("utf-8")
    start = source.index("const renderLiveRound =")
    end = source.index("const renderLobby =", start)
    block = source[start:end]

    assert "shouldPlayHoleTransition" in block
    assert "Number(livePosition) === Number(previousLivePosition) + 1" in block
    assert "previousRound" in block
    assert "playHoleTransition" in block


def test_live_footer_uses_real_round_actions_only():
    page = client().get("/")
    assert page.status_code == 200
    assert b'class="live-footer-actions"' in page.data
    assert b'id="live-nav-more"' in page.data
    assert b'id="advance-live-hole"' in page.data
    assert b'id="live-nav-play"' not in page.data
    assert b'id="live-nav-scorecard"' not in page.data
    assert b'id="live-nav-stats"' not in page.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"LIVE PLAY COMPACT ACTION LAYOUT" in css.data
    assert b".live-footer-actions" in css.data


def test_live_score_card_does_not_show_no_score_status():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const renderScoreCard =")
    end = source.index("const SCRAMBLE_SHOT_TYPES", start)
    block = source[start:end]

    assert "'NO SCORE'" not in block
    assert "meta.hidden = !meta.textContent;" in block


def test_live_stats_shell_is_populated_before_round_math():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const renderLiveHoleStats =")
    end = source.index("const updateReceiptsBadge", start)
    stats_block = source[start:end]

    assert stats_block.index("liveHoleStats.append(") < stats_block.index("try {")
    assert "ROUND STATS" in stats_block
    assert "SCORES IN" in stats_block
    assert "YOUR TOTAL" in stats_block
    assert "TO PAR" in stats_block


def test_live_score_submit_is_compact_inside_score_row():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b".live-score-row .live-score-submit" in css.data
    assert b"width: 88px !important" in css.data
    assert b"grid-column: auto !important" in css.data


def test_live_score_keyboard_survives_background_polling():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")

    assert "const liveScoreDraftInProgress = () =>" in source
    assert "document.activeElement" in source
    assert "active?.classList?.contains('live-score-input')" in source
    assert "data-draft-dirty=\"true\"" in source
    assert "if (liveScoreDraftInProgress()) return;" in source
    assert "input.dataset.draftDirty = 'true'" in source


def test_live_score_adjustments_require_explicit_submit():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const renderScoreCard =")
    end = source.index("const SCRAMBLE_SHOT_TYPES", start)
    score_block = source[start:end]

    assert "submit.className = 'live-score-submit'" in score_block
    assert "'SUBMIT'" in score_block
    assert "'UPDATE'" in score_block
    assert "submit.addEventListener('click', async () =>" in score_block
    assert "minus.addEventListener('click', () =>" in score_block
    assert "plus.addEventListener('click', () =>" in score_block
    assert "await persistScore(next)" not in score_block
    assert "input.addEventListener('change', async" not in score_block


def test_live_stats_show_running_total_and_to_par_not_averages():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const renderLiveHoleStats =")
    end = source.index("const updateReceiptsBadge", start)
    stats_block = source[start:end]

    assert "ROUND STATS" in stats_block
    assert "CURRENT ROUND" in stats_block
    assert "YOUR TOTAL" in stats_block
    assert "TEAM TOTAL" in stats_block
    assert "TO PAR" in stats_block
    assert "AVG SCORE" not in stats_block
    assert "AVG TO PAR" not in stats_block
    assert "round.current_route_position" in stats_block
    assert "viewedRoutePosition" not in stats_block
    assert "const renderLiveHoleStats = (round) =>" in stats_block


def test_browsing_holes_does_not_change_round_stats_source():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")

    assert "renderLiveHoleStats(round);" in source
    assert "renderLiveHoleStats(round, viewedRoutePosition)" not in source

def test_game_action_buttons_use_consistent_label_size():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"WPM ACTION BUTTON TYPE SIZE NORMALIZATION" in css.data
    assert b"#advance-warning-go" in css.data
    assert b"#towel-confirm" in css.data
    assert b"#end-early-yes" in css.data
    assert b"font-size: 1.05rem !important" in css.data


def test_score_remove_button_does_not_consume_grid_row():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    source = css.data.decode("utf-8")
    start = source.index("/* SCORE REMOVE BADGE — NO EXTRA GRID ROW */")
    block = source[start:]

    assert "position: absolute !important;" in block
    assert "grid-row: auto !important;" in block
    assert "width: 32px !important;" in block
    assert "height: 32px !important;" in block
    assert "border-radius: 50% !important;" in block


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

def test_lobby_player_metadata_uses_one_line_per_detail():
    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"lobby-person-meta" in script.data
    assert b"lobby-person-detail" in script.data
    assert b"NO HANDICAP" in script.data
    assert b"NO TEE" in script.data
    assert b"addDetail(String(participant.role || 'player').toUpperCase())" in script.data

    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"LOBBY PLAYER DATA STACK" in css.data
    assert b".lobby-person-meta" in css.data


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


def test_loaded_course_with_complete_pars_hides_par_tracking_setup():
    page = client().get("/")
    assert page.status_code == 200
    assert b'id="setup-par-tracking"' in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"syncSetupParTrackingVisibility" in script.data
    assert b"selectedCourse?.has_complete_pars" in script.data
    assert b"setupParTracking.hidden = loadedCourseHasPars" in script.data

    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    store_source = (root / "who_pushed_me" / "store.py").read_text(
        encoding="utf-8"
    )
    assert 'course["has_complete_pars"]' in store_source
    assert "count(par) AS par_count" in store_source


def test_cached_external_course_selection_returns_full_course_metadata():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    store_source = (root / "who_pushed_me" / "store.py").read_text(
        encoding="utf-8"
    )
    start = store_source.index("    def get_cached_course_by_external_id(")
    end = store_source.index("    @staticmethod\n    def _course_tees", start)
    block = store_source[start:end]

    assert 'return self.get_cached_course(course["id"])' in block
    assert 'course["tees"] = self._course_tees' not in block


def test_cached_course_exposes_and_honors_physical_hole_count():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    store_source = (root / "who_pushed_me" / "store.py").read_text(
        encoding="utf-8"
    )
    assert 'course["hole_count"]' in store_source
    assert "requested_course_hole_count" in store_source
    assert "or detected_hole_count" in store_source


def test_round_setup_sends_route_and_par_tracking_choices():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"start_hole: startHole" in response.data
    assert b"par_tracking_enabled: parSetup !== 'off'" in response.data
    assert b"course_hole_count" in response.data
    assert b"Saving pars..." in response.data


def test_reconnect_role_mismatch_is_rejected():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    store_source = (root / "who_pushed_me" / "store.py").read_text(
        encoding="utf-8"
    )
    start = store_source.index("    def join_round(")
    end = store_source.index("    def promote_spectator_to_player(", start)
    block = store_source[start:end]

    assert 'participant["role"] != participant_role' in block
    assert "reconnect using that role" in block


def test_join_ui_rejects_server_role_mismatch():
    script = client().get("/static/app.js")
    assert script.status_code == 200
    source = script.data.decode("utf-8")
    start = source.index("const joinAsNewParticipant")
    end = source.index("const prepareJoinTeeChoice", start)
    block = source[start:end]

    assert "participant?.role" in block
    assert "Round role mismatch" in block


def test_spectator_score_controls_require_player_role():
    script = client().get("/static/app.js")
    assert script.status_code == 200
    source = script.data.decode("utf-8")
    start = source.index("const renderScoreCard =")
    end = source.index("const SCRAMBLE_SHOT_TYPES", start)
    block = source[start:end]

    assert "round.viewer_role === 'player'" in block
    assert "viewerIsActivePlayer(round)" in block


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


def test_scramble_score_waits_for_contributions_before_advancing():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    store_source = (root / "who_pushed_me" / "store.py").read_text(
        encoding="utf-8"
    )
    start = store_source.index("    def set_score(")
    end = store_source.index("    def remove_score(", start)
    block = store_source[start:end]

    assert 'if round_row["mode"] != "scramble"' in block
    assert "else None" in block


def test_scramble_contributions_prompt_after_score_and_can_be_skipped():
    page = client().get("/")
    script = client().get("/static/app.js")
    assert page.status_code == 200
    assert script.status_code == 200
    assert b'id="scramble-contribution-skip"' in page.data
    assert b"SKIP CONTRIBUTIONS" in page.data

    source = script.data.decode("utf-8")
    assert "skippedScrambleContributionPromptKey" in source
    assert "scrambleContributionPanel?.scrollIntoView" in source
    assert "scrambleContributionSkip?.addEventListener('click'" in source
    assert "await advanceSharedLiveHole();" in source



def test_scramble_contribution_skip_is_styled_as_secondary_action():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    assert b"#scramble-contribution-skip" in css.data
    assert b"background: rgba(5,9,7,.78)" in css.data


def test_mobile_post_hole_ui_is_compact():
    css = client().get("/static/app.css")
    assert css.status_code == 200
    source = css.data.decode("utf-8")
    start = source.index("/* COMPACT POST-HOLE MOBILE UI */")
    block = source[start:]

    assert "grid-template-columns: repeat(5, minmax(0, 1fr))" in block
    assert "score-response-subheading" in block
    assert "display: none !important;" in block
    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in block
    assert "min-height: 36px !important;" in block
    assert "#scramble-contribution-skip" in block

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



def test_round_setup_late_start_keeps_earlier_holes_available_in_live_play():
    page = client().get("/")
    assert page.status_code == 200
    assert b'id="prior-holes-mode"' not in page.data
    assert b'name="prior_holes_mode"' not in page.data
    assert b"EARLIER HOLES" not in page.data
    assert b"Earlier holes stay available in live play" in page.data

    response = client().get("/static/app.js")
    assert response.status_code == 200
    assert b"tracking_start_position: trackingStart" in response.data
    assert b"prior_holes_mode: 'backfill'" in response.data
    assert b"values.get('prior_holes_mode')" not in response.data
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


def test_relationship_question_is_on_registration_not_login():
    page = client().get("/")
    assert page.status_code == 200
    html = page.data.decode("utf-8")

    login_start = html.index('id="login-form"')
    login_end = html.index("</form>", login_start)
    login_block = html[login_start:login_end]
    register_start = html.index('id="register-form"')
    register_end = html.index("</form>", register_start)
    register_block = html[register_start:register_end]

    assert 'name="spouse_type"' not in login_block
    assert 'name="spouse_type"' in register_block
    assert "WHO ARE YOU MARRIED TO?" in register_block
    assert "A WIFE" in register_block
    assert "A HUSBAND" in register_block
    assert "NOT MARRIED" in register_block


def test_registration_sends_spouse_type_and_login_does_not():
    script = client().get("/static/app.js")
    assert script.status_code == 200
    source = script.data.decode("utf-8")

    login_start = source.index("loginForm?.addEventListener('submit'")
    login_end = source.index("registerForm?.addEventListener('submit'", login_start)
    login_block = source[login_start:login_end]
    register_start = login_end
    register_end = source.index("recoverForm?.addEventListener('submit'", register_start)
    register_block = source[register_start:register_end]

    assert "spouse_type: values.get('spouse_type')" not in login_block
    assert "spouse_type: values.get('spouse_type')" in register_block


def test_personalized_messages_resolve_spouse_placeholder():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    api_source = (root / "who_pushed_me" / "api.py").read_text(
        encoding="utf-8"
    )
    start = api_source.index("def user_content_messages():")
    end = api_source.index('@api.get("/admin/status")', start)
    block = api_source[start:end]

    assert '.replace("{spouse}", str(spouse_type))' in block
    assert 'spouse_type in {"wife", "husband"}' in block


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


def test_free_play_exposes_separate_physical_course_layout():
    page = client().get("/")
    assert page.status_code == 200
    assert b'id="course-layout-fieldset"' in page.data
    assert page.data.count(b'name="course_hole_count"') == 2
    assert b"9-HOLE COURSE" in page.data
    assert b"18-HOLE COURSE" in page.data
    assert b"physical course layout" in page.data

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"syncCourseLayoutControl" in script.data
    assert b"selectedPhysicalHoleCount" in script.data
    assert b"body.course_hole_count = selectedPhysicalHoleCount()" in script.data


def test_course_step_separates_round_length_from_physical_layout():
    page = client().get("/")
    assert page.status_code == 200
    html = page.data.decode("utf-8")
    assert html.count('name="holes"') == 2
    assert html.count('name="course_hole_count"') == 2
    assert "ROUND HOLES" in html
    assert "COURSE LAYOUT" in html

    script = client().get("/static/app.js")
    assert script.status_code == 200
    assert b"inferredCourseHoleCount" in script.data
    assert b"Course layout is unknown." in script.data
    assert b"body.course_hole_count = selectedPhysicalHoleCount()" in script.data


def test_live_reaction_panel_is_always_visible():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const appendScoreResponsePanel =")
    end = source.index("const renderScoreCard =", start)
    block = source[start:end]

    assert "document.createElement('section')" in block
    assert "live-score-social-panel" in block
    assert "document.createElement('details')" not in block
    assert "REACTIONS / CHALLENGES" in block


def test_round_banter_uses_one_score_row_per_player_hole():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const renderLiveBanter =")
    end = source.index("const appendLobbyBanterRow =", start)
    banter_block = source[start:end]

    assert "seenScoreKeys" in banter_block
    assert "'score_derived'" in banter_block
    assert "if (eventType === 'score_derived') return false;" not in banter_block
    assert "if (!socialTypes.has(eventType)) return false;" in banter_block
    assert "Boolean(presentation.banter?.text)" not in banter_block
    assert "Boolean(presentation.mascot?.copy)" not in banter_block
    assert "Boolean(presentation.fallback?.text)" not in banter_block
    assert "scoreFeedText(round, event)" in banter_block


def test_live_score_banter_names_subject_and_uses_viewer_perspective():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    assert "const scoreFeedText = (round, event) =>" in source
    assert "'You scored ' + scoreName + '.'" in source
    assert "' scored ' + scoreName + '.'" in source
    assert "const thirdPersonScoreComment = (text) =>" in source


def test_live_polling_does_not_rebuild_open_reactions_challenges_panel():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")

    assert "const liveScoreSocialInteractionInProgress = () =>" in source
    assert "active?.closest?.('.live-score-social-panel')" in source
    assert "data-social-draft-dirty" in source
    assert "liveScoreDraftInProgress()" in source
    assert "|| liveScoreSocialInteractionInProgress()" in source


def test_score_response_sender_combines_selected_reaction_and_comment():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const appendScoreResponsePanel =")
    end = source.index("const renderScoreCard =", start)
    block = source[start:end]

    assert "const sendResponse = async" in block
    assert "/responses" in block
    assert "selectedResponseKind" in block
    assert "selectedResponseKind === 'talk_shit'" in block
    assert "await sendResponse(responseKind, { message })" in block


def test_score_response_and_challenge_events_are_round_banter_items():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const renderLiveBanter =")
    end = source.index("const appendLobbyBanterRow =", start)
    block = source[start:end]

    assert "'score_response'" in block
    assert "'score_challenge'" in block
    assert "eventType === 'score_response'" in source
    assert "eventType === 'score_challenge'" in source


def test_score_banter_never_invents_bare_score_statement():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const scoreFeedText =")
    end = source.index("const APP_BANTER_AVATAR", start)
    block = source[start:end]

    assert "presentation.banter?.text || ''" in block
    assert "if (eventType === 'score_report' && !rawPresentationComment)" in block
    assert "return '';" in block


def test_lobby_round_meta_is_stacked_instead_of_bullet_sentence():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const renderLobby =")
    end = source.index("if (lobbyParticipants)", start)
    block = source[start:end]

    assert "lobbySummary.replaceChildren()" in block
    assert "addSummaryLine('FORMAT'" in block
    assert "addSummaryLine('ROUND'" in block
    assert "addSummaryLine('COURSE'" in block
    assert "lobbySummary.textContent" not in block
    assert " • " not in block


def test_score_lead_stripping_covers_every_score_bucket_without_rewriting_body():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    start = source.index("const stripScoreLead =")
    end = source.index("const thirdPersonScoreComment =", start)
    block = source[start:end]

    assert "stripScoreLead = (text, event)" in block
    assert "ace:" in block
    assert "albatross:" in block
    assert "eagle:" in block
    assert "birdie:" in block
    assert "par:" in block
    assert "bogey:" in block
    assert "double_bogey:" in block
    assert "triple_bogey:" in block
    assert "quad_plus:" in block
    assert "quadruple bogey or worse" in block


def test_quad_plus_approved_copy_does_not_duplicate_score_heading():
    response = client().get("/static/app.js")
    assert response.status_code == 200
    source = response.data.decode("utf-8")
    assert "? stripScoreLead(rawPresentationComment, event)" in source

def test_20260929_approved_score_banter_expansion_is_loaded():
    from who_pushed_me.content.catalog import ContentCatalog

    catalog = ContentCatalog.load()
    expected = {
        "score.report.individual.par": 60,
        "score.report.individual.bogey": 49,
        "score.report.individual.double_bogey": 39,
        "score.report.individual.triple_bogey": 28,
        "score.report.individual.quad_plus": 24,
        "score.report.individual.birdie": 37,
        "score.report.individual.ace": 10,
        "score.report.individual.albatross": 8,
    }
    for event_key, expected_count in expected.items():
        assert len(catalog.eligible_banter(event_key)) == expected_count

    all_rows = catalog.banter
    loaded_ids = {
        row["id"]
        for row in all_rows
        if ".expansion.20260929." in row["id"]
    }
    assert len(loaded_ids) == 136

    first_birdie_rows = [
        row for row in all_rows
        if "score.derived.first_birdie" in row.get("events", [])
        and ".expansion.20260929." in row["id"]
    ]
    assert len(first_birdie_rows) == 7
    assert len(catalog.eligible_banter("score.derived.first_birdie")) == 9

def test_20260930_approved_first_eagle_banter_is_loaded():
    from who_pushed_me.content.catalog import ContentCatalog

    catalog = ContentCatalog.load()
    rows = catalog.eligible_banter("score.derived.first_eagle")
    assert len(rows) == 6
    ids = {row["id"] for row in rows}
    assert "banter.score.first_eagle.expansion.20260930.general.01" in ids
    assert "banter.score.first_eagle.expansion.20260930.spouse.04" in ids

def test_20260930_approved_back_to_back_birdie_banter_is_loaded():
    from who_pushed_me.content.catalog import ContentCatalog

    catalog = ContentCatalog.load()
    rows = catalog.eligible_banter("score.derived.back_to_back_birdies")
    assert len(rows) == 10
    ids = {row["id"] for row in rows}
    assert "banter.score.back_to_back_birdies.expansion.20260930.general.01" in ids
    assert "banter.score.back_to_back_birdies.expansion.20260930.both.08" in ids

def test_20260930_approved_birdie_streak_banter_is_loaded():
    from who_pushed_me.content.catalog import ContentCatalog

    catalog = ContentCatalog.load()
    rows = catalog.eligible_banter("score.derived.birdie_streak_3_plus")
    assert len(rows) == 8
    ids = {row["id"] for row in rows}
    assert "banter.score.birdie_streak_3_plus.expansion.20260930.general.01" in ids
    assert "banter.score.birdie_streak_3_plus.expansion.20260930.both.06" in ids

def test_20260930_approved_bogey_streak_banter_is_loaded():
    from who_pushed_me.content.catalog import ContentCatalog

    catalog = ContentCatalog.load()
    rows = catalog.eligible_banter("score.derived.bogey_streak_3_plus")
    assert len(rows) == 15
    ids = {row["id"] for row in rows}
    assert "banter.score.bogey_streak_3_plus.expansion.20260930.general.01" in ids
    assert "banter.score.bogey_streak_3_plus.expansion.20260930.both.13" in ids
    assert "banter.score.bogey_streak_3_plus.expansion.20260930.drinking.08" in ids

def test_20260930_approved_blowup_hole_banter_is_loaded():
    from who_pushed_me.content.catalog import ContentCatalog

    catalog = ContentCatalog.load()
    rows = catalog.eligible_banter("score.derived.blowup_hole")
    assert len(rows) == 19
    ids = {row["id"] for row in rows}
    assert "banter.score.blowup_hole.expansion.20260930.general.01" in ids
    assert "banter.score.blowup_hole.expansion.20260930.both.18" in ids
    assert "banter.score.blowup_hole.expansion.20260930.general.05" not in ids

def test_20260930_approved_new_leader_banter_is_loaded():
    from who_pushed_me.content.catalog import ContentCatalog

    catalog = ContentCatalog.load()
    rows = catalog.eligible_banter("score.derived.new_leader")
    assert len(rows) == 11
    ids = {row["id"] for row in rows}
    assert "banter.score.new_leader.expansion.20260930.general.01" in ids
    assert "banter.score.new_leader.expansion.20260930.spouse.10" in ids
    assert "banter.score.new_leader.expansion.20260930.spouse.09" not in ids

def test_20260930_approved_tied_lead_banter_is_loaded():
    from who_pushed_me.content.catalog import ContentCatalog

    catalog = ContentCatalog.load()
    rows = catalog.eligible_banter("score.derived.tied_lead")
    assert len(rows) == 18
    ids = {row["id"] for row in rows}
    assert "banter.score.tied_lead.expansion.20260930.general.01" in ids
    assert "banter.score.tied_lead.expansion.20260930.drinking.18" in ids
    assert "banter.score.tied_lead.expansion.20260930.spouse.07" not in ids
    assert "banter.score.tied_lead.expansion.20260930.both.08" not in ids

def test_20260930_approved_lost_lead_banter_is_loaded():
    from who_pushed_me.content.catalog import ContentCatalog

    catalog = ContentCatalog.load()
    rows = catalog.eligible_banter("score.derived.lost_lead")
    assert len(rows) == 19
    ids = {row["id"] for row in rows}
    assert "banter.score.lost_lead.expansion.20260930.general.01" in ids
    assert "banter.score.lost_lead.expansion.20260930.spouse.19" in ids
    assert "banter.score.lost_lead.expansion.20260930.spouse.07" not in ids
    assert "banter.score.lost_lead.expansion.20260930.both.09" not in ids
    assert "banter.score.lost_lead.expansion.20260930.both.20" not in ids

def test_20260930_approved_entered_last_banter_is_loaded():
    from who_pushed_me.content.catalog import ContentCatalog

    catalog = ContentCatalog.load()
    rows = catalog.eligible_banter("score.derived.entered_last")
    assert len(rows) == 13
    ids = {row["id"] for row in rows}
    assert "banter.score.entered_last.expansion.20260930.general.01" in ids
    assert "banter.score.entered_last.expansion.20260930.both.13" in ids
    assert "banter.score.entered_last.expansion.20260930.spouse.10" not in ids
    assert "banter.score.entered_last.expansion.20260930.spouse.11" not in ids

