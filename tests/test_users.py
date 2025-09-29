from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={
        "username": "user123",
        "email": "user@example.com",
        "password": "Password1!",
        "role": "staff"
    })
    assert response.status_code == 201

def test_read_users_as_admin():
    response = client.get("/users", headers={"x-role": "admin"})
    assert response.status_code == 200

def test_update_user_as_admin():
    # create dulu user
    create_res = client.post("/users", json={
        "username": "user456",
        "email": "user2@example.com",
        "password": "Password1!",
        "role": "staff"
    })
    user_id = create_res.json()["id"]

    update_res = client.patch(
        f"/users/{user_id}",
        json={"username": "updateduser"},
        headers={"x-role": "admin"}
    )
    assert update_res.status_code == 200
    assert update_res.json()["username"] == "updateduser"


def test_delete_user_as_admin():
    # create dulu user
    create_res = client.post("/users", json={
        "username": "user789",
        "email": "user3@example.com",
        "password": "Password1!",
        "role": "staff"
    })
    user_id = create_res.json()["id"]

    delete_res = client.delete(f"/users/{user_id}", headers={"x-role": "admin"})
    assert delete_res.status_code == 200
