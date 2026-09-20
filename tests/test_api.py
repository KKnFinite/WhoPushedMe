from uuid import UUID

from app import create_app
from who_pushed_me.courses import CourseHole, CourseSnapshot


class FakeCourseProvider:
    def __init__(self):
        self.calls = []

    def search(self, query, *, limit=10):
        self.calls.append(("search", query, limit))
        return [
            {
                "external_course_id": "provider-1",
                "name": "Provider Muni",
                "city": "Rockford",
                "state": "Illinois",
            }
        ]

    def fetch(self, external_id):
        self.calls.append(("fetch", external_id))
        return CourseSnapshot(
            external_id=external_id,
            name="Provider Muni",
            holes=(
                CourseHole(
                    number=1,
                    par=4,
                    stroke_index=1,
                    tee_yardages={"White": 390},
                ),
            ),
        )


class FakeStore:
    golfer_id = UUID("8db6bcbd-9526-4939-b4be-c94172c32dc0")

    def __init__(self):
        self.calls = []

    def create_golfer(self, display_name):
        return {"id": self.golfer_id, "display_name": display_name, "recovery_key": "ABC-234"}

    def recover_golfer(self, recovery_key):
        self.calls.append(("recover", recovery_key))
        return {"id": self.golfer_id, "display_name": "Kim"}

    def register_account(self, *, username, password, display_name):
        self.calls.append(("register", username, password, display_name))
        return {
            "account": {
                "id": self.golfer_id,
                "username": str(username).lower(),
                "display_name": display_name,
                "is_admin": False,
            },
            "session": {"token": "session-token"},
            "recovery_key": "ABCD-EFGH-JKMP-QRST",
        }

    def login_account(self, *, username, password):
        self.calls.append(("login", username, password))
        return {
            "account": {
                "id": self.golfer_id,
                "username": str(username).lower(),
                "display_name": "Kim",
                "is_admin": False,
            },
            "session": {"token": "session-token"},
        }

    def recover_account_with_key(self, *, recovery_key, new_password):
        self.calls.append(("recover_account", recovery_key, new_password))
        return {
            "account": {
                "id": self.golfer_id,
                "username": "kim",
                "display_name": "Kim",
                "is_admin": False,
            },
            "session": {"token": "replacement-session"},
            "recovery_key": "WXYZ-2345-6789-ABCD",
            "recovery_key_rotated": True,
        }

    def authenticate_session(self, token):
        self.calls.append(("session", token))
        return {
            "id": self.golfer_id,
            "username": "kim",
            "display_name": "Kim",
            "is_admin": False,
        }

    def logout_session(self, token):
        self.calls.append(("logout", token))
        return {"logged_out": True}

    def get_content_preferences(self, golfer_id):
        self.calls.append(("get_preferences", golfer_id))
        return {
            "mini_mascots_enabled": True,
            "trash_talk_enabled": True,
            "max_vulgarity": "normal",
            "themes": {"drinking": True, "wife": True},
        }

    def update_content_preferences(self, golfer_id, patch):
        self.calls.append(("update_preferences", golfer_id, patch))
        return {
            "mini_mascots_enabled": patch.get("mini_mascots_enabled", True),
            "trash_talk_enabled": True,
            "max_vulgarity": patch.get("max_vulgarity", "normal"),
            "themes": {
                "drinking": patch.get("themes", {}).get("drinking", True),
                "wife": True,
            },
        }

    def create_round(
        self,
        golfer_id,
        *,
        mode,
        holes,
        course_id=None,
        free_play_name=None,
        tee_name=None,
    ):
        self.calls.append(
            (
                "create_round",
                golfer_id,
                mode,
                holes,
                course_id,
                free_play_name,
                tee_name,
            )
        )
        return {
            "id": UUID("08966fcb-463a-4c27-8da2-5d2f01d8502d"),
            "active_code": "4321",
            "mode": mode,
            "hole_count": holes,
            "status": "setup",
        }

    def join_round(self, golfer_id, *, code, role, tee_name=None):
        self.calls.append(("join_round", golfer_id, code, role, tee_name))
        return {
            "id": UUID("304b4411-bc80-4652-94b3-350ef2501267"),
            "round_id": UUID("08966fcb-463a-4c27-8da2-5d2f01d8502d"),
            "golfer_id": golfer_id,
            "role": role,
        }

    def get_round(self, golfer_id, code):
        self.calls.append(("get_round", golfer_id, code))
        return {
            "id": UUID("08966fcb-463a-4c27-8da2-5d2f01d8502d"),
            "active_code": code,
            "mode": "individual",
            "hole_count": 18,
            "status": "setup",
            "viewer_role": "player",
            "participants": [],
        }

    def set_status(self, golfer_id, round_id, status):
        self.calls.append(("set_status", golfer_id, round_id, status))
        return {"round_id": round_id, "status": status}

    def search_cached_courses(self, query, *, limit=10):
        self.calls.append(("search_cached_courses", query, limit))
        return [
            {
                "id": UUID("6c2ce930-f82c-4de6-9dbf-4145872d496d"),
                "provider": "opengolfapi",
                "external_course_id": "cached-1",
                "name": "Cached Muni",
            }
        ]

    def get_cached_course_by_external_id(self, external_course_id):
        self.calls.append(("cached_external", external_course_id))
        return None

    def get_cached_course(self, course_id):
        self.calls.append(("get_cached_course", course_id))
        return {
            "id": UUID("6c2ce930-f82c-4de6-9dbf-4145872d496d"),
            "external_course_id": "provider-1",
            "name": "Provider Muni",
            "tees": [
                {
                    "tee_name": "White",
                    "holes_with_tee": 18,
                    "total_yardage": 6200,
                }
            ],
        }

    def cache_course(self, snapshot):
        self.calls.append(("cache_course", snapshot.external_id))
        return UUID("6c2ce930-f82c-4de6-9dbf-4145872d496d")

    def set_participant_tee(self, golfer_id, round_id, tee_name):
        self.calls.append(("set_tee", golfer_id, round_id, tee_name))
        return {
            "round_id": round_id,
            "golfer_id": golfer_id,
            "role": "player",
            "tee_name": tee_name,
        }

    def set_current_hole(self, golfer_id, round_id, hole):
        self.calls.append(("current_hole", golfer_id, round_id, hole))
        return {"round_id": round_id, "current_hole": hole}

    def set_par(self, golfer_id, round_id, hole, par):
        self.calls.append(("par", golfer_id, round_id, hole, par))
        return {"round_id": round_id, "hole": hole, "par": par}

    def set_score(self, golfer_id, round_id, hole, strokes, *, player_participant_id=None):
        self.calls.append(
            ("score", golfer_id, round_id, hole, strokes, player_participant_id)
        )
        return {"hole": hole, "strokes": strokes}


def client_with_store():
    store = FakeStore()
    app = create_app()
    app.config.update(TESTING=True, ROUND_STORE=store)
    return app.test_client(), store


def client_with_store_and_course_provider():
    store = FakeStore()
    provider = FakeCourseProvider()
    app = create_app()
    app.config.update(
        TESTING=True,
        ROUND_STORE=store,
        COURSE_PROVIDER=provider,
    )
    return app.test_client(), store, provider


def test_create_anonymous_golfer_route():
    client, _ = client_with_store()
    response = client.post("/api/golfers", json={"display_name": "Kim"})
    assert response.status_code == 201
    assert response.get_json()["recovery_key"] == "ABC-234"


def test_golf_mutation_requires_recovery_key():
    client, store = client_with_store()
    response = client.put(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/holes/7/score",
        json={"strokes": 5},
    )
    assert response.status_code == 403
    assert not store.calls


def test_score_route_authenticates_and_passes_target_without_moving_hole():
    client, store = client_with_store()
    target = "304b4411-bc80-4652-94b3-350ef2501267"
    response = client.put(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/holes/2/score",
        headers={"X-Recovery-Key": "ABC-234"},
        json={"strokes": 6, "player_participant_id": target},
    )
    assert response.status_code == 200
    assert response.get_json() == {"hole": 2, "strokes": 6}
    assert store.calls[-1] == (
        "score",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        2,
        6,
        target,
    )

def test_preferences_route_requires_authentication():
    client, store = client_with_store()
    response = client.get("/api/preferences")

    assert response.status_code == 403
    assert not store.calls


def test_preferences_patch_passes_data_driven_theme_settings():
    client, store = client_with_store()
    response = client.patch(
        "/api/preferences",
        headers={"X-Recovery-Key": "ABC-234"},
        json={
            "mini_mascots_enabled": False,
            "max_vulgarity": "brutal",
            "themes": {"drinking": False},
        },
    )

    assert response.status_code == 200
    assert response.get_json()["mini_mascots_enabled"] is False
    assert response.get_json()["max_vulgarity"] == "brutal"
    assert response.get_json()["themes"]["drinking"] is False
    assert store.calls[-1] == (
        "update_preferences",
        store.golfer_id,
        {
            "mini_mascots_enabled": False,
            "max_vulgarity": "brutal",
            "themes": {"drinking": False},
        },
    )

def test_round_store_uses_unpooled_database_url_when_pooled_is_absent(monkeypatch):
    from who_pushed_me.store import RoundStore

    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv(
        "DATABASE_URL_UNPOOLED",
        "postgresql://example.invalid/wpm",
    )

    assert RoundStore().database_url == "postgresql://example.invalid/wpm"

def test_register_account_returns_one_time_recovery_key_and_session():
    client, store = client_with_store()
    response = client.post(
        "/api/auth/register",
        json={
            "username": "Kim",
            "password": "correct horse battery staple",
            "display_name": "Kim",
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["account"]["username"] == "kim"
    assert payload["session"]["token"] == "session-token"
    assert payload["recovery_key"] == "ABCD-EFGH-JKMP-QRST"
    assert store.calls[-1] == (
        "register",
        "Kim",
        "correct horse battery staple",
        "Kim",
    )


def test_login_account_returns_session_without_recovery_key():
    client, store = client_with_store()
    response = client.post(
        "/api/auth/login",
        json={
            "username": "Kim",
            "password": "correct horse battery staple",
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["session"]["token"] == "session-token"
    assert "recovery_key" not in payload
    assert store.calls[-1] == (
        "login",
        "Kim",
        "correct horse battery staple",
    )


def test_auth_me_requires_bearer_session():
    client, store = client_with_store()

    missing = client.get("/api/auth/me")
    assert missing.status_code == 403

    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer session-token"},
    )
    assert response.status_code == 200
    assert response.get_json()["username"] == "kim"
    assert store.calls[-1] == ("session", "session-token")

def test_auth_logout_revokes_current_bearer_session():
    client, store = client_with_store()
    response = client.post(
        "/api/auth/logout",
        headers={"Authorization": "Bearer session-token"},
    )

    assert response.status_code == 200
    assert response.get_json() == {"logged_out": True}
    assert store.calls[-2:] == [
        ("session", "session-token"),
        ("logout", "session-token"),
    ]

def test_recovery_key_resets_password_rotates_key_and_returns_session():
    client, store = client_with_store()
    response = client.post(
        "/api/auth/recover",
        json={
            "recovery_key": "ABCD-EFGH-JKMP-QRST",
            "new_password": "a brand new password",
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["session"]["token"] == "replacement-session"
    assert payload["recovery_key"] == "WXYZ-2345-6789-ABCD"
    assert payload["recovery_key_rotated"] is True
    assert store.calls[-1] == (
        "recover_account",
        "ABCD-EFGH-JKMP-QRST",
        "a brand new password",
    )

def test_score_route_accepts_new_bearer_session_authentication():
    client, store = client_with_store()
    target = "304b4411-bc80-4652-94b3-350ef2501267"
    response = client.put(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/holes/2/score",
        headers={"Authorization": "Bearer session-token"},
        json={"strokes": 5, "player_participant_id": target},
    )

    assert response.status_code == 200
    assert store.calls[-2] == ("session", "session-token")
    assert store.calls[-1] == (
        "score",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        2,
        5,
        target,
    )

def test_create_round_with_bearer_session_enters_setup_lobby():
    client, store = client_with_store()
    response = client.post(
        "/api/rounds",
        headers={"Authorization": "Bearer session-token"},
        json={
            "mode": "scramble",
            "holes": 9,
            "free_play_name": "Saturday Shitshow",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["status"] == "setup"
    assert response.get_json()["active_code"] == "4321"
    assert store.calls[-1] == (
        "create_round",
        store.golfer_id,
        "scramble",
        9,
        None,
        "Saturday Shitshow",
        None,
    )


def test_join_and_lobby_routes_use_bearer_session():
    client, store = client_with_store()

    joined = client.post(
        "/api/rounds/join",
        headers={"Authorization": "Bearer session-token"},
        json={"code": "4321", "role": "spectator"},
    )
    assert joined.status_code == 201
    assert joined.get_json()["role"] == "spectator"

    lobby = client.get(
        "/api/rounds/code/4321",
        headers={"Authorization": "Bearer session-token"},
    )
    assert lobby.status_code == 200
    assert lobby.get_json()["active_code"] == "4321"
    assert store.calls[-1] == ("get_round", store.golfer_id, "4321")


def test_any_player_session_can_start_setup_round():
    client, store = client_with_store()
    response = client.patch(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/status",
        headers={"Authorization": "Bearer session-token"},
        json={"status": "active"},
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "active"
    assert store.calls[-1] == (
        "set_status",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        "active",
    )

def test_course_search_returns_cache_first_then_provider():
    client, store, provider = client_with_store_and_course_provider()
    response = client.get(
        "/api/courses/search?q=muni&limit=5",
        headers={"Authorization": "Bearer session-token"},
    )

    assert response.status_code == 200
    results = response.get_json()["results"]
    assert results[0]["source"] == "cache"
    assert results[0]["name"] == "Cached Muni"
    assert results[1]["source"] == "provider"
    assert results[1]["external_course_id"] == "provider-1"
    assert provider.calls[-1] == ("search", "muni", 5)


def test_select_provider_course_caches_it_before_round_setup():
    client, store, provider = client_with_store_and_course_provider()
    response = client.post(
        "/api/courses/select",
        headers={"Authorization": "Bearer session-token"},
        json={"external_course_id": "provider-1"},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["name"] == "Provider Muni"
    assert payload["tees"][0]["tee_name"] == "White"
    assert ("fetch", "provider-1") in provider.calls
    assert ("cache_course", "provider-1") in store.calls


def test_player_can_set_tee_before_round_start():
    client, store = client_with_store()
    response = client.patch(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/tee",
        headers={"Authorization": "Bearer session-token"},
        json={"tee_name": "White"},
    )

    assert response.status_code == 200
    assert response.get_json()["tee_name"] == "White"
    assert store.calls[-1] == (
        "set_tee",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        "White",
    )

def test_course_round_creation_passes_cached_course_and_tee():
    client, store = client_with_store()
    course_id = "6c2ce930-f82c-4de6-9dbf-4145872d496d"
    response = client.post(
        "/api/rounds",
        headers={"Authorization": "Bearer session-token"},
        json={
            "mode": "individual",
            "holes": 18,
            "course_id": course_id,
            "tee_name": "White",
        },
    )

    assert response.status_code == 201
    assert store.calls[-1] == (
        "create_round",
        store.golfer_id,
        "individual",
        18,
        course_id,
        None,
        "White",
    )


def test_join_round_can_carry_initial_tee_choice():
    client, store = client_with_store()
    response = client.post(
        "/api/rounds/join",
        headers={"Authorization": "Bearer session-token"},
        json={
            "code": "4321",
            "role": "player",
            "tee_name": "White",
        },
    )

    assert response.status_code == 201
    assert store.calls[-1] == (
        "join_round",
        store.golfer_id,
        "4321",
        "player",
        "White",
    )

def test_live_scorecard_can_advance_shared_hole_without_touching_scores():
    client, store = client_with_store()
    response = client.patch(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/current-hole",
        headers={"Authorization": "Bearer session-token"},
        json={"hole": 4},
    )

    assert response.status_code == 200
    assert response.get_json()["current_hole"] == 4
    assert store.calls[-1] == (
        "current_hole",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        4,
    )


def test_live_scorecard_can_report_or_push_par():
    client, store = client_with_store()
    response = client.put(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/holes/4/par",
        headers={"Authorization": "Bearer session-token"},
        json={"par": 5},
    )

    assert response.status_code == 200
    assert response.get_json()["par"] == 5
    assert store.calls[-1] == (
        "par",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        4,
        5,
    )

