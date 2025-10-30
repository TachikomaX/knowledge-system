def test_create_tag(client, test_user):
    import uuid
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    tag_name = f"TestTag-{uuid.uuid4().hex[:8]}"
    resp = client.post("/api/tags", json={"name": tag_name}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    tag_id = resp.json()["data"]["id"]
    assert tag_id > 0
    # 清理测试数据
    del_resp = client.delete(f"/api/tags/{tag_id}", headers=headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["code"] == 0


def test_get_tags(client, test_user):
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    resp = client.get("/api/tags", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0


def test_update_tag(client, test_user):
    import uuid
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    tag_name = f"TagToUpdate-{uuid.uuid4().hex[:8]}"
    # 创建标签
    resp = client.post("/api/tags", json={"name": tag_name}, headers=headers)
    tag_id = resp.json()["data"]["id"]
    # 更新
    new_name = f"UpdatedTag-{uuid.uuid4().hex[:8]}"
    resp = client.put(f"/api/tags/{tag_id}",
                      json={"name": new_name},
                      headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    assert resp.json()["data"]["name"] == new_name
    # 清理测试数据
    del_resp = client.delete(f"/api/tags/{tag_id}", headers=headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["code"] == 0


def test_delete_tag(client, test_user):
    import uuid
    headers = {"Authorization": f"Bearer {test_user['token']}"}
    tag_name = f"TagToDelete-{uuid.uuid4().hex[:8]}"
    # 创建标签
    resp = client.post("/api/tags", json={"name": tag_name}, headers=headers)
    tag_id = resp.json()["data"]["id"]
    # 删除
    del_resp = client.delete(f"/api/tags/{tag_id}", headers=headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["code"] == 0
