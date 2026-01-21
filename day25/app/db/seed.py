from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models.user import User
from app.core.security import get_password_hash

# Optional: create tables if not already
from app.db.base import Base
Base.metadata.create_all(bind=engine)

def seed_users():
    db: Session = SessionLocal()

    # List of test users
    test_users = [
        {"email": "admin@example.com", "password": "admin123", "role": "admin"},
        {"email": "user1@example.com", "password": "user1234", "role": "user"},
        {"email": "user2@example.com", "password": "user1234", "role": "user"},
        {"email": "qa@example.com", "password": "qa12345", "role": "user"},
    ]

    for u in test_users:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if existing:
            print(f"Skipping existing user: {u['email']}")
            continue

        user = User(
            email=u["email"],
            hashed_password=get_password_hash(u["password"]),
            role=u["role"]
        )
        db.add(user)
        print(f"Added user: {u['email']} ({u['role']})")

    db.commit()
    db.close()
    print("Seeding complete!")

if __name__ == "__main__":
    seed_users()
