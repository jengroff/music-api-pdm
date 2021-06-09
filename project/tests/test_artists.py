import json


def test_create_artist(test_app_with_db):
    response = test_app_with_db.post(
        "/artists", data=json.dumps({"name": "the name", "spid": "the spid"})
    )

    assert response.status_code == 201
    assert response.json()["name"] == "the name"
    assert response.json()["spid"] == "the spid"


def test_create_artists_invalid_json(test_app):
    response = test_app.post("/artists", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "spid"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_read_artist(test_app_with_db):
    response = test_app_with_db.post(
        "/artists", data=json.dumps({"name": "the name", "spid": "the spid"})
    )
    id = response.json()["id"]

    response = test_app_with_db.get(f"/artists/{id}")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == id


def test_read_all_artists(test_app_with_db):
    response = test_app_with_db.post(
        "/artists", data=json.dumps({"name": "the name", "spid": "the spid"})
    )
    id = response.json()["id"]

    response = test_app_with_db.get(f"/artists")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == id, response_list))) == 1