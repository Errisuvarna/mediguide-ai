def test_list_doctors(client):
    resp = client.get("/api/doctors")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_filter_doctors_by_department(client):
    depts = client.get("/api/departments").json()
    dept_id = depts[0]["id"]
    resp = client.get("/api/doctors", params={"department_id": dept_id})
    assert resp.status_code == 200
    for doc in resp.json():
        assert doc["department_id"] == dept_id
