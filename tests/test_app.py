from app import create_app


def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_home_loads():
    response = client().get("/")
    assert response.status_code == 200
    assert b"WHO PUSHED ME?!" in response.data
    assert b"WE SUCK TOGETHER" in response.data


def test_health():
    response = client().get("/health")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["status"] == "ok"
    assert payload["service"] == "who-pushed-me-scorecard"


def test_invalid_mode_redirects_home():
    response = client().get("/new-round?mode=chaos")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_scramble_requires_two_players():
    response = client().post(
        "/round-preview",
        data={
            "mode": "scramble",
            "course": "Test Course",
            "holes": "18",
            "player_1": "Khris",
        },
    )
    assert response.status_code == 400
    assert b"at least two victims" in response.data


def test_round_preview_accepts_scramble_setup():
    response = client().post(
        "/round-preview",
        data={
            "mode": "scramble",
            "course": "Test Course",
            "holes": "18",
            "player_1": "Khris",
            "player_2": "Grayson",
            "player_3": "Mike",
            "player_4": "Steve",
        },
    )
    assert response.status_code == 200
    assert b"Test Course" in response.data
    assert b"Grayson" in response.data
