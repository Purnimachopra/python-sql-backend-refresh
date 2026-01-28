# tests/test_auth_flow.py
import pytest
import uuid
from app.models.user import User
from app.core.security import get_password_hash

@pytest.fixture
def create_test_user(db):
    """Fixture to create a test user."""
    user = User(
        email=f"user_{uuid.uuid4()}@example.com",
        hashed_password=get_password_hash("user1234"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def test_auth_flow(client, db, create_test_user):
    user = create_test_user

    # -------------------------------
    # 1️⃣ LOGIN
    # -------------------------------
    login_resp = client.post(
        "/auth/login",
        json={"email": user.email, "password": "user1234"}
    )
    assert login_resp.status_code == 200, login_resp.text
    tokens = login_resp.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    print("Access token after login :", access_token)
    print("Refresh token after login :", refresh_token)
    # -------------------------------
    # 2️⃣ REFRESH TOKEN ROTATION
    # -------------------------------
    refresh_resp = client.post(
        "/auth/refreshToken",
        json={"refresh_token": refresh_token}  # send old token
    )
    assert refresh_resp.status_code == 200, refresh_resp.text
    new_tokens = refresh_resp.json()
    new_access_token = new_tokens["access_token"]
    new_refresh_token = new_tokens["refresh_token"]
    print("New Access token:", new_access_token)
    print("New Refresh token:", new_refresh_token)

    # 2️⃣a Check that new refresh token is different
    assert new_refresh_token != refresh_token

    # 2️⃣b Old refresh token should be revoked
    reuse_old_resp = client.post(
        "/auth/refreshToken",
        json={"refresh_token": refresh_token}  # old token
    )
    assert reuse_old_resp.status_code in (401, 403)

    # -------------------------------
    # 3️⃣ LOGOUT
    # -------------------------------
    logout_resp = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {new_access_token}"},
        json={"refresh_token": new_refresh_token}
    )
    assert logout_resp.status_code == 200
    assert logout_resp.json().get("message") == "Logged out successfully"

    # -------------------------------
    # 4️⃣ VERIFY POST-LOGOUT REFRESH FAILS
    # -------------------------------
    refresh_after_logout = client.post(
        "/auth/refreshToken",
        json={"refresh_token": new_refresh_token}
    )
    assert refresh_after_logout.status_code in (401, 403)
