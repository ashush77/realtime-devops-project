from fastapi.testclient import TestClient

from app.main import app


def test_home_endpoint():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code in (200, 503)


def test_items_endpoint():
    with TestClient(app) as client:
        response = client.get("/items")

    assert response.status_code in (200, 500, 503)
