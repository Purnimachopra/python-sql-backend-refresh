import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app, get_db
from models import Base, User
from auth import create_access_token, get_password_hash

# In-memory database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def create_user(username: str, role: str):
    db = TestingSessionLocal()
    user = User(
        username=username,
        hashed_password=get_password_hash("password"),
        role=role
    )
    db.add(user)
    db.commit()
    db.close()



def get_token(username: str, role: str):
    return create_access_token(
        data={
            "sub": username,
            "role": role
        }
    )


def test_admin_can_access_admin_endpoint():
    create_user("admin1", "admin")
    token = get_token("admin1", "admin")

    response = client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    
def test_user_cannot_access_admin_endpoint():
    create_user("user1", "user")
    token = get_token("user1", "user")

    response = client.get(
        "/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403

def test_no_token_is_rejected():
    response = client.get("/admin/users")
    assert response.status_code == 401
