def test_submit_feedback(client):
    resp = client.post("/api/feedback", json={
        "name": "Jane Doe", "rating": 5, "comments": "Great service!",
    })
    assert resp.status_code == 201
    assert resp.json()["rating"] == 5


def test_feedback_rating_bounds(client):
    resp = client.post("/api/feedback", json={"rating": 6})
    assert resp.status_code == 422
