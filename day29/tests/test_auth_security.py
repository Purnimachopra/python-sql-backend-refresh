import pytest
import uuid
from app.models.user import User
from app.services.auth_tokens import get_refresh_token, create_refresh_token
from app.core.security import get_password_hash, create_access_token


def test_refresh_token_reuse_forbidden(client, db):
    # 1️⃣ Create user
    user = User(email=f"user_{uuid.uuid4()}@example.com",
                hashed_password=get_password_hash("password123"),
                is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)

    # 2️⃣ Login: get initial refresh token
    refresh_token_obj = create_refresh_token(db, user.id)
    access_token = create_access_token({"sub": str(user.id)})

    # 3️⃣ Use refresh token to rotate (new token)
    rotate_resp = client.post(
        "/auth/refreshToken",
        json={"refresh_token": refresh_token_obj.token}
    )
    assert rotate_resp.status_code == 200
    new_refresh_token = rotate_resp.json()["refresh_token"]

    # 4️⃣ Attempt reuse of old token (should fail)
    reuse_resp = client.post(
        "/auth/refreshToken",
        json={"refresh_token": refresh_token_obj.token}
    )

    assert reuse_resp.status_code in (401, 403)
    assert "revoked" in reuse_resp.text.lower() or "invalid" in reuse_resp.text.lower()


def test_logout_revokes_refresh_token(client, db):
    # 1️⃣ Create user
    user = User(email="secure_logout@example.com",
                hashed_password=get_password_hash("password123"),
                is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)

    # 2️⃣ Login: get refresh token
    refresh_token_obj = create_refresh_token(db, user.id)
    access_token = create_access_token({"sub": str(user.id)})

    # 3️⃣ Logout using token
    logout_resp = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"refresh_token": refresh_token_obj.token}
    )

    assert logout_resp.status_code == 200

    # 4️⃣ Attempt refresh with revoked token
    refresh_after_logout = client.post(
        "/auth/refreshToken",
        json={"refresh_token": refresh_token_obj.token}
    )

    # Should fail because token is revoked
    assert refresh_after_logout.status_code in (401, 403)
