# tests/test_activity_logs.py
import pytest
from config import db, create_test_app
from models.ActivityLog import ActivityLog
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = create_test_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def auth_header(app, user_id=1):
    with app.app_context():
        token = create_access_token(identity=str(user_id))  
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def test_create_log(client):
    res = client.post("/activity-logs/", json={"user_id": 1, "action": "Login"})
    assert res.status_code == 201

def test_get_all_logs(client):
    client.post("/activity-logs/", json={"user_id": 1, "action": "Test"})
    res = client.get("/activity-logs/")
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_get_log_by_id(client):
    post = client.post("/activity-logs/", json={"user_id": 1, "action": "Fetch"})
    log_id = post.get_json()["id"]
    res = client.get(f"/activity-logs/{log_id}")
    assert res.status_code == 200

def test_update_log(client):
    post = client.post("/activity-logs/", json={"user_id": 1, "action": "To be updated"})
    log_id = post.get_json()["id"]
    res = client.put(f"/activity-logs/{log_id}", json={"action": "Updated"})
    assert res.status_code == 200

def test_delete_log(client):
    post = client.post("/activity-logs/", json={"user_id": 1, "action": "To delete"})
    log_id = post.get_json()["id"]
    res = client.delete(f"/activity-logs/{log_id}")
    assert res.status_code == 200

def test_get_logs_for_user(client, app):
    with app.app_context():
        db.session.add(ActivityLog(user_id=42, action="Secret action"))
        db.session.commit()

    headers = auth_header(app, user_id=42)
    res = client.get("/activity-logs/user", headers=headers)

    assert res.status_code == 200


def test_get_logs_for_user_unauthorized(client):
    res = client.get("/activity-logs/user")
    assert res.status_code == 401
    




