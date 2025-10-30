import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def test_user(client):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass"
    }
    client.post("/api/users/register", json=user_data)
    resp = client.post("/api/users/login",
                       json={
                           "email": user_data["email"],
                           "password": user_data["password"]
                       })
    token = resp.json()["data"]["access_token"]
    return {"token": token, "user": user_data}
