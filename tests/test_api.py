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
        start_hole=1,
        end_hole=None,
        course_hole_count=None,
        par_tracking_enabled=True,
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
                start_hole,
                end_hole,
                course_hole_count,
                par_tracking_enabled,
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

    def get_round(
        self,
        golfer_id,
        code=None,
        *,
        round_id=None,
        event_limit=100,
    ):
        lookup = round_id if round_id is not None else code
        self.calls.append(("get_round", golfer_id, lookup))
        return {
            "id": UUID("08966fcb-463a-4c27-8da2-5d2f01d8502d"),
            "active_code": code or "4321",
            "mode": "individual",
            "hole_count": 18,
            "status": "setup",
            "viewer_role": "player",
            "participants": [],
        }

    def set_status(
        self,
        golfer_id,
        round_id,
        status,
        *,
        finish_incomplete=False,
    ):
        call = ("set_status", golfer_id, round_id, status)
        if finish_incomplete:
            call += (True,)
        self.calls.append(call)
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

    def promote_spectator_to_player(self, golfer_id, round_id, *, tee_name=None):
        self.calls.append(("join_play", golfer_id, round_id, tee_name))
        return {
            "round_id": round_id,
            "role": "player",
            "tee_name": tee_name,
            "tracked_from_position": 7,
        }

    def list_claimable_round_only_players(self, golfer_id, code):
        self.calls.append(("claimable_players", golfer_id, code))
        return {
            "round_id": "08966fcb-463a-4c27-8da2-5d2f01d8502d",
            "active_code": code,
            "players": [
                {
                    "participant_id": "304b4411-bc80-4652-94b3-350ef2501267",
                    "display_name": "Mike",
                    "tee_name": "White",
                }
            ],
        }

    def add_round_only_player(
        self,
        golfer_id,
        round_id,
        *,
        display_name,
        tee_name=None,
    ):
        self.calls.append(
            ("add_round_only", golfer_id, round_id, display_name, tee_name)
        )
        return {
            "id": "304b4411-bc80-4652-94b3-350ef2501267",
            "round_id": round_id,
            "role": "player",
            "display_name": display_name,
            "tee_name": tee_name,
            "round_only": True,
        }

    def claim_round_only_player(
        self,
        golfer_id,
        round_id,
        participant_id,
    ):
        self.calls.append(
            ("claim_round_only", golfer_id, round_id, participant_id)
        )
        return {
            "id": participant_id,
            "round_id": round_id,
            "role": "player",
            "display_name": "Kim",
            "round_only": False,
        }

    def set_participation_state(self, golfer_id, round_id, state, *, reason=None):
        self.calls.append(("participation", golfer_id, round_id, state, reason))
        return {
            "round_id": round_id,
            "participant_id": "participant-1",
            "participation_state": state,
        }

    def set_end_early_vote(self, golfer_id, round_id, vote):
        self.calls.append(("end_early_vote", golfer_id, round_id, vote))
        return {
            "round_id": round_id,
            "status": "active",
            "end_early": {
                "proposal_active": True,
                "required_count": 2,
                "yes_count": 1,
            },
        }

    def set_current_hole(self, golfer_id, round_id, hole):
        self.calls.append(("current_hole", golfer_id, round_id, hole))
        return {"round_id": round_id, "current_hole": hole}

    def set_par(self, golfer_id, round_id, hole, par):
        self.calls.append(("par", golfer_id, round_id, hole, par))
        return {"round_id": round_id, "hole": hole, "par": par}

    def set_scramble_contribution(
        self,
        golfer_id,
        round_id,
        hole,
        shot_type,
        player_participant_id,
    ):
        self.calls.append(
            (
                "contribution",
                golfer_id,
                round_id,
                hole,
                shot_type,
                player_participant_id,
            )
        )
        return {
            "round_id": round_id,
            "hole": hole,
            "shot_type": shot_type,
            "player_participant_id": player_participant_id,
        }

    def set_event_reaction(self, golfer_id, round_id, event_id, reaction_kind):
        self.calls.append(
            ("set_reaction", golfer_id, round_id, event_id, reaction_kind)
        )
        return {
            "event_id": event_id,
            "actor_participant_id": "participant-1",
            "reaction_kind": reaction_kind,
        }

    def remove_event_reaction(self, golfer_id, round_id, event_id):
        self.calls.append(("remove_reaction", golfer_id, round_id, event_id))
        return {"event_id": event_id, "removed": True}

    def set_score_challenge(
        self,
        golfer_id,
        round_id,
        score_event_id,
        *,
        proposed_score=None,
        comment=None,
    ):
        self.calls.append(
            (
                "score_challenge",
                golfer_id,
                round_id,
                score_event_id,
                proposed_score,
                comment,
            )
        )
        return {
            "score_event_id": score_event_id,
            "status": "active",
            "proposed_score": proposed_score,
            "comment": comment,
        }

    def withdraw_score_challenge(self, golfer_id, round_id, score_event_id):
        self.calls.append(
            ("withdraw_score_challenge", golfer_id, round_id, score_event_id)
        )
        return {"score_event_id": score_event_id, "status": "withdrawn"}

    def add_score_response(
        self,
        golfer_id,
        round_id,
        score_event_id,
        *,
        response_kind,
        message=None,
        target_participant_id=None,
    ):
        self.calls.append(
            (
                "score_response",
                golfer_id,
                round_id,
                score_event_id,
                response_kind,
                message,
                target_participant_id,
            )
        )
        return {
            "id": UUID("4f99b4cf-4a74-48a9-b29e-908c0d2d36fc"),
            "event_type": "score_response",
            "reply_to_event_id": score_event_id,
            "data": {
                "response_kind": response_kind,
                "message": message,
                "target_participant_id": target_participant_id,
            },
        }

    def add_social_event(
        self,
        golfer_id,
        round_id,
        event_type,
        *,
        hole=None,
        data=None,
    ):
        self.calls.append(
            (
                "social",
                golfer_id,
                round_id,
                event_type,
                hole,
                data,
            )
        )
        return {
            "id": UUID("fe89db21-0f73-46bc-a598-69891c14a91e"),
            "event_type": event_type,
            "hole_number": hole,
            "data": data or {},
        }

    def set_score(self, golfer_id, round_id, hole, strokes, *, player_participant_id=None):
        self.calls.append(
            ("score", golfer_id, round_id, hole, strokes, player_participant_id)
        )
        return {"hole": hole, "strokes": strokes}

    def remove_score(self, golfer_id, round_id, hole, *, player_participant_id=None):
        self.calls.append(
            ("remove_score", golfer_id, round_id, hole, player_participant_id)
        )
        return {"hole": hole, "removed_strokes": 6}


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

def test_remove_score_route_preserves_explicit_target():
    client, store = client_with_store()
    target = "304b4411-bc80-4652-94b3-350ef2501267"

    response = client.delete(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/positions/2/score",
        headers={"Authorization": "Bearer session-token"},
        json={"player_participant_id": target},
    )

    assert response.status_code == 200
    assert response.get_json()["removed_strokes"] == 6
    assert store.calls[-1] == (
        "remove_score",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        2,
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
        1,
        None,
        None,
        True,
    )


def test_create_round_passes_explicit_route_setup():
    client, store = client_with_store()
    response = client.post(
        "/api/rounds",
        headers={"Authorization": "Bearer session-token"},
        json={
            "mode": "scramble",
            "holes": 18,
            "free_play_name": "Shotgun Disaster",
            "start_hole": 14,
            "course_hole_count": 18,
            "par_tracking_enabled": False,
        },
    )

    assert response.status_code == 201
    assert store.calls[-1] == (
        "create_round",
        store.golfer_id,
        "scramble",
        18,
        None,
        "Shotgun Disaster",
        None,
        14,
        None,
        18,
        False,
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
        1,
        None,
        None,
        True,
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

def test_spectator_can_join_play_mid_round_with_tee():
    client, store = client_with_store()
    response = client.patch(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/join-play",
        headers={"Authorization": "Bearer session-token"},
        json={"tee_name": "White"},
    )

    assert response.status_code == 200
    assert response.get_json()["role"] == "player"
    assert store.calls[-1] == (
        "join_play",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        "White",
    )


def test_join_flow_can_list_claimable_round_only_players():
    client, store = client_with_store()
    response = client.get(
        "/api/rounds/code/4321/claimable-players",
        headers={"Authorization": "Bearer session-token"},
    )

    assert response.status_code == 200
    assert response.get_json()["players"][0]["display_name"] == "Mike"
    assert store.calls[-1] == (
        "claimable_players",
        store.golfer_id,
        "4321",
    )


def test_active_player_can_add_round_only_golfer():
    client, store = client_with_store()
    response = client.post(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/round-only-players",
        headers={"Authorization": "Bearer session-token"},
        json={"display_name": "Mike", "tee_name": "White"},
    )

    assert response.status_code == 201
    assert response.get_json()["round_only"] is True
    assert store.calls[-1] == (
        "add_round_only",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        "Mike",
        "White",
    )


def test_account_can_claim_exact_round_only_participant():
    client, store = client_with_store()
    participant_id = "304b4411-bc80-4652-94b3-350ef2501267"
    response = client.patch(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/claim-player",
        headers={"Authorization": "Bearer session-token"},
        json={"participant_id": participant_id},
    )

    assert response.status_code == 200
    assert response.get_json()["round_only"] is False
    assert store.calls[-1] == (
        "claim_round_only",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        participant_id,
    )


def test_player_can_throw_in_the_towel_with_optional_reason():
    client, store = client_with_store()
    response = client.patch(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/participation",
        headers={"Authorization": "Bearer session-token"},
        json={"state": "withdrew", "reason": "I have seen enough."},
    )

    assert response.status_code == 200
    assert response.get_json()["participation_state"] == "withdrew"
    assert store.calls[-1] == (
        "participation",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        "withdrew",
        "I have seen enough.",
    )


def test_withdrawn_player_can_return_to_round():
    client, store = client_with_store()
    response = client.patch(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/participation",
        headers={"Authorization": "Bearer session-token"},
        json={"state": "active"},
    )

    assert response.status_code == 200
    assert response.get_json()["participation_state"] == "active"
    assert store.calls[-1] == (
        "participation",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        "active",
        None,
    )


def test_player_can_vote_to_end_round_early():
    client, store = client_with_store()
    response = client.patch(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/end-early-vote",
        headers={"Authorization": "Bearer session-token"},
        json={"vote": True},
    )

    assert response.status_code == 200
    assert response.get_json()["end_early"]["yes_count"] == 1
    assert store.calls[-1] == (
        "end_early_vote",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        True,
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


def test_active_hole_route_accepts_route_position_payload():
    client, store = client_with_store()
    response = client.patch(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/current-hole",
        headers={"Authorization": "Bearer session-token"},
        json={"route_position": 7},
    )

    assert response.status_code == 200
    assert store.calls[-1] == (
        "current_hole",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        7,
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

def test_bag_of_bullshit_route_passes_targeted_callout_payload():
    client, store = client_with_store()
    target = "304b4411-bc80-4652-94b3-350ef2501267"
    response = client.post(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/events",
        headers={"Authorization": "Bearer session-token"},
        json={
            "type": "callout",
            "hole": 6,
            "data": {
                "target_participant_id": target,
                "situation": "water_shot",
                "message": "Splashdown.",
            },
        },
    )

    assert response.status_code == 201
    assert store.calls[-1] == (
        "social",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        "callout",
        6,
        {
            "target_participant_id": target,
            "situation": "water_shot",
            "message": "Splashdown.",
        },
    )


def test_bag_of_bullshit_route_passes_reaction_payload():
    client, store = client_with_store()
    response = client.post(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/events",
        headers={"Authorization": "Bearer session-token"},
        json={
            "type": "reaction",
            "hole": 6,
            "data": {"reaction": "bullshit"},
        },
    )

    assert response.status_code == 201
    assert store.calls[-1] == (
        "social",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        "reaction",
        6,
        {"reaction": "bullshit"},
    )

def test_scramble_contribution_route_tracks_selected_player():
    client, store = client_with_store()
    target = "304b4411-bc80-4652-94b3-350ef2501267"
    response = client.put(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/holes/7/contributions/drive",
        headers={"Authorization": "Bearer session-token"},
        json={"player_participant_id": target},
    )

    assert response.status_code == 200
    assert store.calls[-1] == (
        "contribution",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        7,
        "drive",
        target,
    )


def test_finish_incomplete_requires_explicit_api_confirmation():
    client, store = client_with_store()
    response = client.patch(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/status",
        headers={"Authorization": "Bearer session-token"},
        json={"status": "completed", "finish_incomplete": True},
    )

    assert response.status_code == 200
    assert store.calls[-1] == (
        "set_status",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        "completed",
        True,
    )


def test_complete_round_status_can_return_final_results():
    client, store = client_with_store()
    response = client.patch(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/status",
        headers={"Authorization": "Bearer session-token"},
        json={"status": "completed"},
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "completed"
    assert store.calls[-1] == (
        "set_status",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        "completed",
    )

def test_final_damage_report_download_requires_completed_round():
    client, store = client_with_store()

    response = client.get(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/report.pdf",
        headers={"Authorization": "Bearer session-token"},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == (
        "final damage report is only available after the round is completed"
    )


def test_final_damage_report_download_returns_pdf_attachment():
    client, store = client_with_store()

    def completed_round(
        golfer_id,
        code=None,
        *,
        round_id=None,
        event_limit=100,
    ):
        assert event_limit is None
        return {
            "id": UUID("08966fcb-463a-4c27-8da2-5d2f01d8502d"),
            "active_code": "4321",
            "status": "completed",
            "mode": "scramble",
            "hole_count": 1,
            "course": None,
            "free_play_name": "Test Disaster",
            "viewer_role": "player",
            "viewer_participant_id": "p1",
            "participants": [
                {"id": "p1", "role": "player", "display_name": "Kim"},
            ],
            "pars": [{"hole_number": 1, "par": 4}],
            "scores": [
                {
                    "hole_number": 1,
                    "score_scope": "team",
                    "player_participant_id": None,
                    "strokes": 5,
                }
            ],
            "contributions": [],
            "results": {
                "mode": "scramble",
                "complete": True,
                "score_count": 1,
                "missing_scores": 0,
                "team_total": 5,
                "players": [],
            },
            "events": [],
        }

    store.get_round = completed_round

    response = client.get(
        "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/report.pdf",
        headers={"Authorization": "Bearer session-token"},
    )

    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert response.data.startswith(b"%PDF-")
    assert "who-pushed-me-4321-final-damage-report.pdf" in (
        response.headers["Content-Disposition"]
    )

def test_event_reaction_route_sets_one_current_reaction():
    client, store = client_with_store()
    event_id = "b9aa9b19-78f7-4c6d-8e2d-0a0a0b0b0c0d"

    response = client.put(
        (
            "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/"
            f"events/{event_id}/reaction"
        ),
        headers={"Authorization": "Bearer session-token"},
        json={"reaction": "bullshit"},
    )

    assert response.status_code == 200
    assert store.calls[-1] == (
        "set_reaction",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        event_id,
        "bullshit",
    )


def test_event_reaction_route_can_remove_current_reaction():
    client, store = client_with_store()
    event_id = "b9aa9b19-78f7-4c6d-8e2d-0a0a0b0b0c0d"

    response = client.delete(
        (
            "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/"
            f"events/{event_id}/reaction"
        ),
        headers={"Authorization": "Bearer session-token"},
    )

    assert response.status_code == 200
    assert store.calls[-1] == (
        "remove_reaction",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        event_id,
    )


def test_score_challenge_route_accepts_proposed_score_and_comment():
    client, store = client_with_store()
    event_id = "b9aa9b19-78f7-4c6d-8e2d-0a0a0b0b0c0d"

    response = client.put(
        (
            "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/"
            f"score-events/{event_id}/challenge"
        ),
        headers={"Authorization": "Bearer session-token"},
        json={"proposed_score": 5, "comment": "That was a five."},
    )

    assert response.status_code == 200
    assert store.calls[-1] == (
        "score_challenge",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        event_id,
        5,
        "That was a five.",
    )


def test_score_challenge_route_can_withdraw():
    client, store = client_with_store()
    event_id = "b9aa9b19-78f7-4c6d-8e2d-0a0a0b0b0c0d"

    response = client.delete(
        (
            "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/"
            f"score-events/{event_id}/challenge"
        ),
        headers={"Authorization": "Bearer session-token"},
    )

    assert response.status_code == 200
    assert store.calls[-1] == (
        "withdraw_score_challenge",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        event_id,
    )


def test_score_response_route_links_reply_to_specific_score_event():
    client, store = client_with_store()
    score_event_id = "b9aa9b19-78f7-4c6d-8e2d-0a0a0b0b0c0d"
    target = "304b4411-bc80-4652-94b3-350ef2501267"

    response = client.post(
        (
            "/api/rounds/08966fcb-463a-4c27-8da2-5d2f01d8502d/"
            f"score-events/{score_event_id}/responses"
        ),
        headers={"Authorization": "Bearer session-token"},
        json={
            "response_kind": "blame",
            "message": "That was all Pat.",
            "target_participant_id": target,
        },
    )

    assert response.status_code == 201
    assert store.calls[-1] == (
        "score_response",
        store.golfer_id,
        "08966fcb-463a-4c27-8da2-5d2f01d8502d",
        score_event_id,
        "blame",
        "That was all Pat.",
        target,
    )

