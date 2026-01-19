from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user():
    raise NotImplementedError("Implemented on Day 20")


"""Interview answer:

“Why use dependencies for DB?”
→ Proper lifecycle management + testability"""