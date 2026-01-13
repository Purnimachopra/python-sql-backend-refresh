from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Loan Repayment API running"


def test_repayment_schedule_success():
    payload = {
        "principal": 100000,
        "annual_rate": 10,
        "tenure_years": 1
    }

    response = client.post("/repayment-schedule", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "schedule" in data
    assert len(data["schedule"]) == 12
    assert data["schedule"][0]["month"] == 1


def test_repayment_schedule_invalid_input():
    payload = {
        "principal": -50000,
        "annual_rate": 10,
        "tenure_years": 1
    }

    response = client.post("/repayment-schedule", json=payload)
    assert response.status_code == 400
