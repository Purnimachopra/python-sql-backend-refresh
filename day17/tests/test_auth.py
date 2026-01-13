def test_login_and_get_token(client):
    # First register a user
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200

    # Login
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
