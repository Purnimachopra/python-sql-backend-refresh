# tests/test_auth_logout.py
import pytest
import uuid
from app.models.user import User
from app.core.security import get_password_hash

@pytest.fixture
def create_test_user(db):
    """Fixture to create a test user in the database."""
    user = User(
        email=f"user_{uuid.uuid4()}@example.com",
        hashed_password=get_password_hash("user1234"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def test_logout_revokes_refresh_token(client, db, create_test_user):
    user = create_test_user

    # 1️⃣ Login to get access and refresh tokens
    login_resp = client.post(
        "/auth/login",
        json={"email": user.email, "password": "user1234"}
    )
    assert login_resp.status_code == 200, login_resp.text
    tokens = login_resp.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # 2️⃣ Call logout endpoint with JSON body and Authorization header
    logout_resp = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"refresh_token": refresh_token}  # must be string, not function
    )
    assert logout_resp.status_code == 200
    body = logout_resp.json()
    assert body.get("message") == "Logged out successfully"

    # 3️⃣ Verify that using the same refresh token fails
    refresh_after_logout = client.post(
        "/auth/refreshToken",
        json={"refresh_token": refresh_token}  # old token
    )

    # Depending on your endpoint, revoked tokens may return 403 or 401
    assert refresh_after_logout.status_code in (401, 403)
