def test_register(client):
    resp = client.post("/api/users/register",
                       json={
                           "username": "testuser2",
                           "email": "testuser2@example.com",
                           "password": "testpass2"
                       })
    assert resp.status_code == 200
    assert resp.json()["code"] == 0 or resp.json()["code"] == 1001 # 允许重复注册


def test_register_duplicate(client):
    # 重复注册用户名
    resp = client.post("/api/users/register",
                       json={
                           "username": "testuser2",
                           "email": "testuser3@example.com",
                           "password": "testpass2"
                       })
    assert resp.status_code == 200
    assert resp.json()["code"] != 0
    # 重复注册邮箱
    resp = client.post("/api/users/register",
                       json={
                           "username": "testuser3",
                           "email": "testuser2@example.com",
                           "password": "testpass2"
                       })
    assert resp.status_code == 200
    assert resp.json()["code"] != 0


def test_login_success(client):
    resp = client.post("/api/users/login",
                       json={
                           "email": "testuser2@example.com",
                           "password": "testpass2"
                       })
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    assert "access_token" in resp.json()["data"]


def test_login_fail(client):
    resp = client.post("/api/users/login",
                       json={
                           "email": "testuser2@example.com",
                           "password": "wrongpass"
                       })
    assert resp.status_code == 200
    assert resp.json()["code"] != 0
