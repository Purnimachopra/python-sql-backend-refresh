def test_create_loan_without_token_fails(client):
    response = client.post(
        "/loan",
        json={
            "principal": 100000,
            "annual_rate": 9,
            "tenure_years": 2
        }
    )

    assert response.status_code == 401


def test_create_loan_with_valid_token(client):
    # Register
    client.post(
        "/register",
        json={"username": "authuser", "password": "secret"}
    )

    # Login
    token_response = client.post(
        "/token",
        data={"username": "authuser", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = token_response.json()["access_token"]

    # Call protected endpoint
    response = client.post(
        "/loan",
        json={
            "principal": 200000,
            "annual_rate": 8,
            "tenure_years": 3
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "emi" in response.json()


def test_create_loan_with_invalid_token_fails(client):
    response = client.post(
        "/loan",
        json={
            "principal": 100000,
            "annual_rate": 9,
            "tenure_years": 2
        },
        headers={"Authorization": "Bearer abc.def.xyz"}
    )

    assert response.status_code == 401
