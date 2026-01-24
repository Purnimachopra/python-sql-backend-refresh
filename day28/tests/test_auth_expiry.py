import pytest
import uuid
from datetime import datetime, timedelta, timezone
from app.models.user import User
from app.services.auth_tokens import create_refresh_token, get_refresh_token
from app.core.security import create_access_token, get_password_hash
from jose import jwt
from app.core.config import settings


def test_access_token_expiry(client, db):
    # 1️⃣ Create user
    email = f"user_{uuid.uuid4()}@example.com"
    user = User(email=email,
                hashed_password=get_password_hash("password123"),
                is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)

    # 2️⃣ # 🔥 Manually create an expired JWT
    payload = {
        "sub": str(user.id),
        "exp": datetime.now(timezone.utc) - timedelta(minutes=5)
    }

    expired_access_token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    # 3️⃣ Attempt protected endpoint (logout requires auth)
    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {expired_access_token}"},
        json={"refresh_token": create_refresh_token(db, user.id).token}
    )

    assert response.status_code == 401
    assert "detail" in response.json()


def test_refresh_token_expiry(client, db):
    # 1️⃣ Create user
    user = User(email=f"user_{uuid.uuid4()}@example.com",
                hashed_password=get_password_hash("password123"),
                is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)

    # 2️⃣ Create a refresh token that expired yesterday
    expired_refresh = create_refresh_token(db, user.id)
    expired_refresh.expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    db.commit()

    # 3️⃣ Attempt refresh
    response = client.post(
        "/auth/refreshToken",
        json={"refresh_token": expired_refresh.token}
    )

    # Should fail with 401 Unauthorized
    assert response.status_code == 401
    assert "Invalid or expired refresh token" in response.text or "detail" in response.json()
