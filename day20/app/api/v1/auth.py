from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from app.core.dependencies import get_db
from app.models.user import User

from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import SessionLocal
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)
    
"""class RegisterRequest(BaseModel):
    email: EmailStr
    password: str  """

@router.post("/register")
def register(payload: UserCreate, db: Session = Depends(get_db)):

     # 🔍 TEMPORARY DEBUG (VERY IMPORTANT)
    print("PASSWORD VALUE:", payload.password)
    print("PASSWORD TYPE:", type(payload.password))
    print("PASSWORD LENGTH:", len(payload.password.encode("utf-8")))
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="User exists")

    user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        role="admin"
    )
    db.add(user)
    db.commit()
    return {"message": "Admin created"}

@router.post("/login")
def login(
    payload: UserCreate, db: Session = Depends(get_db)
):
    print("in login api , data received is ",payload.email,"  and ",payload.password)
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    print("user validated")
    token = create_access_token({"sub": user.email})
    print("token generated successfully")
    return {"access_token": token, "token_type": "bearer"}
