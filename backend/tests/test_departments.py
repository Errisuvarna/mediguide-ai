def test_list_departments(client):
    resp = client.get("/api/departments")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]


def test_search_departments(client):
    resp = client.get("/api/departments", params={"search": "cardio"})
    assert resp.status_code == 200
    data = resp.json()
    assert any("cardio" in d["name"].lower() for d in data)
