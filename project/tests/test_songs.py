import json


def test_create_song(test_app_with_db):
    response = test_app_with_db.post(
        "/songs", data=json.dumps({"name": "the name", "spid": "the spid"})
    )

    assert response.status_code == 201
    assert response.json()["name"] == "the name"
    assert response.json()["spid"] == "the spid"


def test_create_songs_invalid_json(test_app):
    response = test_app.post("/songs", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "spid"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_read_song(test_app_with_db):
    response = test_app_with_db.post(
        "/songs", data=json.dumps({"name": "the name", "spid": "the spid"})
    )
    id = response.json()["id"]

    response = test_app_with_db.get(f"/songs/{id}")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == id


def test_read_song_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/songs/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Object does not exist"

    response = test_app_with_db.get("/songs/0")
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


def test_read_all_songs(test_app_with_db):
    response = test_app_with_db.post(
        "/songs", data=json.dumps({"name": "the name", "spid": "the spid"})
    )
    id = response.json()["id"]

    response = test_app_with_db.get("/songs")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == id, response_list))) == 1


def test_remove_song(test_app_with_db):
    response = test_app_with_db.post(
        "/songs", data=json.dumps({"name": "the name", "spid": "the spid"})
    )
    id = response.json()["id"]

    response = test_app_with_db.delete(f"/songs/{id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Deleted song {id}"


def test_remove_song_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/songs/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Song not found"

    response = test_app_with_db.delete("/songs/0")
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


def test_update_song(test_app_with_db):
    response = test_app_with_db.post(
        "/songs", data=json.dumps({"name": "the name", "spid": "the spid"})
    )
    id = response.json()["id"]

    response = test_app_with_db.put(
        f"/songs/{id}",
        data=json.dumps({"name": "updated name!", "spid": "updated spid!"}),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == id
    assert response_dict["name"] == "updated name!"
    assert response_dict["spid"] == "updated spid!"
    assert response_dict["created_at"]
