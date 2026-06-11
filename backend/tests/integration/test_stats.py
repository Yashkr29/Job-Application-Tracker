from fastapi.testclient import TestClient


def test_stats_overview(client: TestClient, auth_headers: dict[str, str]) -> None:
    """Stats overview returns application aggregates."""
    client.post(
        "/api/applications/",
        headers=auth_headers,
        json={"title": "Data Engineer", "company": "Globex", "status": "OFFER", "priority": "dream"},
    )
    response = client.get("/api/stats/overview", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total"] == 1
    assert data["by_status"]["OFFER"] == 1

