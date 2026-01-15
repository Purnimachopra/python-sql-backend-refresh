#Routers = Thin Controllers

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud.user import create_user
from app.core.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
def create(user: UserCreate, db: Session = Depends(get_db)):
    hashed = get_password_hash(user.password)
    return create_user(db, user.email, hashed)
