def test_register_and_login(client):
    payload = {
        "full_name": "Test Admin",
        "email": "test.admin@example.com",
        "password": "SecurePass123",
        "role": "admin",
    }
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 201
    assert resp.json()["email"] == payload["email"]

    login_resp = client.post("/api/auth/login", json={
        "email": payload["email"], "password": payload["password"],
    })
    assert login_resp.status_code == 200
    body = login_resp.json()
    assert "access_token" in body
    assert body["user"]["role"] == "admin"


def test_login_wrong_password(client):
    resp = client.post("/api/auth/login", json={
        "email": "test.admin@example.com", "password": "WrongPassword",
    })
    assert resp.status_code == 401
