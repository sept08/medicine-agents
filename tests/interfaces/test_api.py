from fastapi.testclient import TestClient

from medicine_agents.interfaces.api import create_app


def test_health_endpoint(tmp_path) -> None:
    client = TestClient(create_app(data_dir=tmp_path))
    assert client.get("/health").json() == {"status": "ok", "stage": "S1"}


def test_create_order_returns_saved_synthetic_package(tmp_path) -> None:
    client = TestClient(create_app(data_dir=tmp_path))
    response = client.post(
        "/api/orders",
        json={
            "disease_code": "DKD",
            "difficulty": "basic",
            "target_audience": "undergraduate",
            "teaching_objectives": ["识别关键临床线索"],
        },
    )

    assert response.status_code == 201
    assert response.json()["synthetic"] is True
    assert response.json()["status"] == "draft"
    case_id = response.json()["case_id"]
    assert (tmp_path / "cases" / case_id / "current.json").exists()


def test_create_order_rejects_empty_objectives(tmp_path) -> None:
    client = TestClient(create_app(data_dir=tmp_path))
    response = client.post(
        "/api/orders",
        json={
            "disease_code": "DKD",
            "difficulty": "basic",
            "target_audience": "undergraduate",
            "teaching_objectives": [],
        },
    )

    assert response.status_code == 422