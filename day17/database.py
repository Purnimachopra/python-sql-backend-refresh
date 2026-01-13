from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./loan.db"  
print("🔴 database.py loaded → DISK database configured:", DATABASE_URL)
#This creates a real file on disk:
#loan.db  ← stored permanently
"""Data stays even after program stops

Tests write real data

Tests affect each other ❌"""

"""database.py is NOT changed for tests on purpose.
👉 Tests override the dependency, not the configuration file.

FastAPI decides which database to use at runtime via dependencies, not via database.py
"""

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
