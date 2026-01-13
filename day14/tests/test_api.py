from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_create_loan_success():
    payload = {
        "principal": 150000,
        "annual_rate": 8.5,
        "tenure_years": 3
    }

    response = client.post("/loan", json=payload)

    assert response.status_code == 200

    data = response.json()
    assert data["principal"] == 150000
    assert data["annual_rate"] == 8.5
    assert data["tenure_years"] == 3
    assert "emi" in data
    assert data["emi"] > 0
    assert "id" in data


def test_create_loan_invalid_principal():
    payload = {
        "principal": -100000,
        "annual_rate": 9,
        "tenure_years": 2
    }

    response = client.post("/loan", json=payload)
    assert response.status_code == 400
