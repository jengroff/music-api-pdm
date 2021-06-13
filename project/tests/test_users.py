import json


def test_create_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users", data=json.dumps({
            "email": "the email",
            "password": "the password",
            "role": "Admin"
        })
    )

    assert response.status_code == 201
    assert response.json()["email"] == "the email"
    assert response.json()["password"] == "the password"
    assert response.json()["role"] == "Admin"


def test_create_users_invalid_json(test_app):
    response = test_app.post("/users", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "email"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "password"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_read_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users", data=json.dumps({
            "email": "the email",
            "password": "the password",
            "role": "Admin"
        })
    )
    id = response.json()["id"]

    response = test_app_with_db.get(f"/users/{id}")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == id


def test_read_user_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Object does not exist"

    response = test_app_with_db.get("/users/0")
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


def test_read_all_users(test_app_with_db):
    response = test_app_with_db.post(
        "/users", data=json.dumps({
            "email": "the email",
            "password": "the password",
            "role": "Admin"
        })
    )
    id = response.json()["id"]

    response = test_app_with_db.get(f"/users")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == id, response_list))) == 1


def test_remove_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users", data=json.dumps({
            "email": "the email",
            "password": "the password",
            "role": "Admin"
        })
    )
    id = response.json()["id"]

    response = test_app_with_db.delete(f"/users/{id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Deleted user {id}"


def test_remove_user_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == f"User not found"

    response = test_app_with_db.delete("/users/0")
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


def test_update_user(test_app_with_db):
    response = test_app_with_db.post(
        "/users", data=json.dumps({
            "email": "the email",
            "password": "the password",
            "role": "Admin"
        })
    )
    id = response.json()["id"]

    response = test_app_with_db.put(
        f"/users/{id}",
        data=json.dumps({
            "email": "updated email",
            "password": "updated password"
        })
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == id
    assert response_dict["email"] == "updated email"
    assert response_dict["password"] == "updated password"
    assert response_dict["created_at"]
