import json


def test_create_playlist(test_app_with_db):
    response = test_app_with_db.post(
        "/playlists", data=json.dumps({"name": "the name"})
    )

    assert response.status_code == 201
    assert response.json()["name"] == "the name"


def test_create_playlists_invalid_json(test_app):
    response = test_app.post("/playlists", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_read_playlist(test_app_with_db):
    response = test_app_with_db.post(
        "/playlists", data=json.dumps({"name": "the name"})
    )
    playlist_id = response.json()["id"]

    response = test_app_with_db.get(f"/playlists/{playlist_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == playlist_id


def test_read_playlist_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/playlists/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Object does not exist"

    response = test_app_with_db.get("/playlists/0")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_read_all_playlists(test_app_with_db):
    response = test_app_with_db.post(
        "/playlists", data=json.dumps({"name": "the name"})
    )
    playlist_id = response.json()["id"]

    response = test_app_with_db.get(f"/playlists/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == playlist_id, response_list))) == 1
