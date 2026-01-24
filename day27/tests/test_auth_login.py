
#import pytest
from app.models.user import User
from app.core.security import get_password_hash

#@pytest.fixture(scope="module")
def test_login_success(client,db):

    # Create user first (direct DB or signup endpoint)
    user = User(
        email="user1@example.com",
        hashed_password=get_password_hash("user1234"),
        is_active=True
    )
    db.add(user)
    db.commit()

    response = client.post(
         "/auth/login",
        json={
            "email": "user1@example.com",
            "password": "user1234"
        }
    )
  

    assert response.status_code == 200
    body = response.json()

    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "bearer"
