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
    assert b"APP UNDER CONSTRUCTION, DUMBASS." in response.data
    assert b"SIGN IN" in response.data
    assert b"CREATE ACCOUNT" in response.data
    assert b"RECOVER" in response.data
    assert b"Settings" in response.data
    assert b"EVERY ASSHOLE FOR THEMSELVES" in response.data
    assert b"WE SUCK TOGETHER" in response.data
    assert b"FIND A COURSE" in response.data
    assert b"FREE PLAY" in response.data
    assert b"YOUR TEE" in response.data
    assert b"START THE SHITSHOW" in response.data
    assert b"LIVE SCORECARD" in response.data
    assert b"REPORT PAR" in response.data
    assert b"LATEST RECEIPT" in response.data
    assert b"BAG OF BULLSHIT" in response.data
    assert b"CALL SOMEONE OUT" in response.data
    assert b"NICE FUCKING SHOT" in response.data
    assert b"CALL YOUR SHOT" in response.data
    assert b"YOU WON'T" in response.data
    assert b"EXCUSE DEPARTMENT" in response.data
    assert b"OPEN MIC" in response.data
    assert b"REACTIONS" in response.data
    assert b"SCRAMBLE CONTRIBUTIONS" in response.data
    assert b"FINISH THE DISASTER" in response.data
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
    assert b"wpm-shell-v10" in response.data
    assert response.headers["Cache-Control"] == "no-cache"
