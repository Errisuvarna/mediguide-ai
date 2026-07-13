def test_analytics_shape(client):
    client.post("/api/chat", json={
        "session_id": "analytics-session", "message": "Where is the lab?", "language": "en",
    })
    resp = client.get("/api/analytics")
    assert resp.status_code == 200
    body = resp.json()
    assert "summary" in body
    assert "charts" in body
    assert body["summary"]["total_queries"] >= 1
