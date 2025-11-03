def test_create_note(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    resp = client.post("/api/notes",
                       json={
                           "title": "Test Note",
                           "content": "Note content",
                           "summary": "Summary"
                       },
                       headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    note_id = resp.json()["data"]["id"]
    assert note_id > 0


def test_update_note(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    # 创建笔记
    resp = client.post("/api/notes",
                       json={
                           "title": "Note to update",
                           "content": "Old content",
                           "summary": "Old summary"
                       },
                       headers=headers)
    note_id = resp.json()["data"]["id"]
    # 更新
    resp = client.put(f"/api/notes/{note_id}",
                      json={
                          "title": "Updated title",
                          "content": "Updated content"
                      },
                      headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    assert resp.json()["data"]["title"] == "Updated title"


def test_delete_note(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    # 创建笔记
    resp = client.post("/api/notes",
                       json={
                           "title": "Note to delete",
                           "content": "Delete me"
                       },
                       headers=headers)
    note_id = resp.json()["data"]["id"]
    # 删除
    resp = client.delete(f"/api/notes/{note_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0


def test_search_notes(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    resp = client.get("/api/notes/search?q=Test", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
