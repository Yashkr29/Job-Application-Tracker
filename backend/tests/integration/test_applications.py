from fastapi.testclient import TestClient


def test_application_crud(client: TestClient, auth_headers: dict[str, str]) -> None:
    """User can create, list, update status, and delete an application."""
    created = client.post(
        "/api/applications/",
        headers=auth_headers,
        json={"title": "Backend Engineer", "company": "Acme", "status": "SAVED", "priority": "high"},
    )
    assert created.status_code == 200
    app_id = created.json()["data"]["id"]

    listed = client.get("/api/applications/", headers=auth_headers)
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] == 1

    updated = client.patch(f"/api/applications/{app_id}/status", headers=auth_headers, json={"status": "APPLIED"})
    assert updated.status_code == 200
    assert updated.json()["data"]["status"] == "APPLIED"

    detail = client.get(f"/api/applications/{app_id}", headers=auth_headers)
    assert detail.status_code == 200
    assert len(detail.json()["data"]["status_history"]) == 2

    deleted = client.delete(f"/api/applications/{app_id}", headers=auth_headers)
    assert deleted.status_code == 200

