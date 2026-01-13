from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

"""create_engine → Creates a connection to the database

sessionmaker → Creates database sessions (used to run queries)

declarative_base → Base class for all ORM models (tables)"""

DATABASE_URL = "sqlite:///./loan.db"

"""Uses SQLite

./loan.db → Database file will be created in the project root

If file doesn’t exist → SQLite creates it automatically"""

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
"""engine = core connection to the database

check_same_thread=False

Required for SQLite

Allows database access from multiple threads

Very important when using FastAPI or pytest

❌ Without this → you’ll get runtime threading errors"""

SessionLocal = sessionmaker(bind=engine)
"""SessionLocal() → gives a new database session

Each request / operation gets its own session

Used to:

Read data

Insert rows

Update / delete records"""

Base = declarative_base()

"""Create Base class for models
All ORM models (tables) must inherit from Base
SQLAlchemy uses this to:

Track tables

Create schema using Base.metadata.create_all()"""

"""Base  → defines tables
engine → connects to DB
SessionLocal → runs queries
loan.db → actual database file"""