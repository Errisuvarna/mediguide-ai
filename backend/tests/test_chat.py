def test_chat_basic_query(client):
    resp = client.post("/api/chat", json={
        "session_id": "test-session-1",
        "message": "How do I get an itemized bill?",
        "language": "en",
        "is_voice": False,
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["session_id"] == "test-session-1"
    assert len(body["reply"]) > 0
    assert body["is_emergency"] is False


def test_chat_emergency_detection(client):
    resp = client.post("/api/chat", json={
        "session_id": "test-session-2",
        "message": "I am having chest pain right now",
        "language": "en",
        "is_voice": False,
    })
    assert resp.status_code == 200
    assert resp.json()["is_emergency"] is True


def test_chat_history_persisted(client):
    client.post("/api/chat", json={
        "session_id": "test-session-3", "message": "Where is the pharmacy?", "language": "en",
    })
    resp = client.get("/api/history", params={"session_id": "test-session-3"})
    assert resp.status_code == 200
    history = resp.json()
    assert len(history) == 2  # user + assistant
    assert history[0]["role"] == "user"
