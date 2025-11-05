from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity: at least one known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Math Club"
    email = "test_user@example.com"

    # Ensure clean starting state for this email
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant added
    all_activities = client.get("/activities").json()
    assert email in all_activities[activity]["participants"]

    # Unregister
    resp2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp2.status_code == 200
    assert "Unregistered" in resp2.json().get("message", "")

    # Verify participant removed
    all_activities = client.get("/activities").json()
    assert email not in all_activities[activity]["participants"]

    # Cleanup (defensive)
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
