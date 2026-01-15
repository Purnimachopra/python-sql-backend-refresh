import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


from app import app, get_db
from database import Base
from fastapi.testclient import TestClient

# In-memory SQLite database for tests
#SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

SQLALCHEMY_DATABASE_URL = "sqlite://"
print("🟢 TEST MODE → In-memory database configured")

"""This creates a database:

Only in RAM

No file

Deleted automatically when program ends

Clean DB
✔ Independent tests
✔ CI-safe
"""

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def client():
    # Create tables
    print("🟢 Creating fresh in-memory tables")
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        print("🟢 Using IN-MEMORY DB session")
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    """This tells FastAPI:“Ignore the original get_db.
    Use this one instead.”"""

    """Even though database.py exists:

    FastAPI never calls get_db() from app.py

    It calls the overridden version"""

    """database.py defines defaults.
Tests override behavior at runtime."""

    with TestClient(app) as c:
        yield c
    print("🟢 Dropping in-memory tables")
    Base.metadata.drop_all(bind=engine)
