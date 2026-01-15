from fastapi import FastAPI
from app.api.v1 import users, auth, admin
from app.db.session import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)
print("MAIN LOADED")
app = FastAPI(title="Backend API")

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(admin.router)
