from uuid import UUID

from app import create_app


class FakeStore:
    golfer_id = UUID("8db6bcbd-9526-4939-b4be-c94172c32dc0")

    def __init__(self):
        self.calls = []

    def create_golfer(self, display_name):
        return {"id": self.golfer_id, "display_name": display_name, "recovery_key": "ABC-234"}

    def recover_golfer(self, recovery_key):
        self.calls.append(("recover", recovery_key))
        return {"id": self.golfer_id, "display_name": "Kim"}

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

