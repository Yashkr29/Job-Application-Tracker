from fastapi.testclient import TestClient


def test_register_login_and_me(client: TestClient) -> None:
    """User can register, login, and fetch profile."""
    register = client.post(
        "/api/auth/register",
        json={"email": "auth@example.com", "name": "Auth User", "password": "password123"},
    )
    assert register.status_code == 201
    assert register.json()["success"] is True

    login = client.post("/api/auth/login", json={"email": "auth@example.com", "password": "password123"})
    assert login.status_code == 200
    token = login.json()["data"]["access_token"]

    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["data"]["email"] == "auth@example.com"


def test_login_lockout_after_failures(client: TestClient) -> None:
    """Account locks after repeated failed logins."""
    client.post(
        "/api/auth/register",
        json={"email": "lock@example.com", "name": "Lock User", "password": "password123"},
    )
    for _ in range(5):
        response = client.post("/api/auth/login", json={"email": "lock@example.com", "password": "wrong"})
        assert response.status_code == 401
    locked = client.post("/api/auth/login", json={"email": "lock@example.com", "password": "password123"})
    assert locked.status_code == 423

