import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.seed import seed_users

# -------------------------------
# Seed QA users before all tests
# -------------------------------
@pytest.fixture(scope="module", autouse=True)
def setup_seed():
    seed_users()
    yield

# -------------------------------
# FastAPI TestClient fixture
# -------------------------------
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# -------------------------------
# Normal user token fixture
# -------------------------------
@pytest.fixture(scope="module")
def user_token(client):
    response = client.post(
         "/auth/login",
        json={"email": "user1@example.com", "password": "user1234"}
    )
    assert response.status_code == 200
    #token = response.json()["access_token"]
   # assert token
    return response.json()["access_token"]

# -------------------------------
# Admin token fixture
# -------------------------------
@pytest.fixture(scope="module")
def admin_token(client):
    response = client.post(
        "/auth/login",
        json={"email":  "admin@example.com", "password": "admin123"}
    )
    assert response.status_code == 200
    #token = response.json()["access_token"]
   # assert token  # ensure token exists
    return response.json()["access_token"]

# -------------------------------
# Test 1: Admin /users/me
# -------------------------------
def test_users_me_admin(client, admin_token):
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
   # assert data["email"] == "admin@example.com"
    assert data["role"] == "admin"
   # assert data["is_active"] is True


# -------------------------------
# Test 2: Admin /admin/dashboard
# -------------------------------
def test_admin_dashboard_access(client, admin_token):
    response = client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    #data = response.json()
    #assert "Welcome admin" in data["message"]

# -------------------------------
# Test 3: Normal user cannot access admin
# -------------------------------
def test_user_cannot_access_admin(client, user_token):
    response = client.get(
        "/admin/dashboard",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
    #data = response.json()
   # assert data["detail"] == "Not authorized"


# -------------------------------
# Test 4: Normal user /users/me
# -------------------------------
def test_users_me_user(client, user_token):
    print("Executing test_users_me_user")
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
   # assert data["email"] == "user1@example.com"
    assert data["role"] == "user"
