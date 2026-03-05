from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_login_success():
    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password():
    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "wrong"
    })
    assert response.status_code == 401


def test_login_wrong_username():
    response = client.post("/auth/login", json={
        "username": "hacker",
        "password": "admin123"
    })
    assert response.status_code == 401


def test_protected_endpoint_without_token():
    response = client.get("/audit")
    assert response.status_code == 401


def test_protected_endpoint_with_invalid_token():
    response = client.get("/audit", headers={
        "Authorization": "Bearer token_falso_123"
    })
    assert response.status_code == 401
