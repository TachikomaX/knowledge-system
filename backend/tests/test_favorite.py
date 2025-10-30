def test_add_and_remove_favorite(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    # 创建笔记
    resp = client.post("/api/notes",
                       json={
                           "title": "FavNote",
                           "content": "FavContent"
                       },
                       headers=headers)
    note_id = resp.json()["data"]["id"]
    # 收藏
    resp = client.post(f"/api/favorites/{note_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    # 检查收藏状态
    resp = client.get(f"/api/favorites/{note_id}/status", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["is_favorited"] is True
    # 取消收藏
    resp = client.delete(f"/api/favorites/{note_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    # 再查状态
    resp = client.get(f"/api/favorites/{note_id}/status", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["is_favorited"] is False


def test_get_user_favorite_notes(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    resp = client.get("/api/favorites", headers=headers)
    assert resp.status_code == 200
    assert "data" in resp.json()
