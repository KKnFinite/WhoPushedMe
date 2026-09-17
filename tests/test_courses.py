from who_pushed_me.courses import OpenGolfAPI


def test_opengolfapi_adapter_normalizes_course_holes(monkeypatch):
    client = OpenGolfAPI()

    def fake_get(path, query=None):
        if path.endswith("/holes"):
            return {
                "holes": [
                    {
                        "number": 1,
                        "par": 4,
                        "handicap_index": 7,
                        "yardages": {"blue": 401, "white": 372},
                    }
                ]
            }
        return {"id": "course-123", "name": "Muni National"}

    monkeypatch.setattr(client, "_get", fake_get)
    snapshot = client.fetch("course-123")

    assert snapshot.external_id == "course-123"
    assert snapshot.name == "Muni National"
    assert snapshot.holes[0].par == 4
    assert snapshot.holes[0].stroke_index == 7
    assert snapshot.holes[0].tee_yardages == {"blue": 401, "white": 372}
