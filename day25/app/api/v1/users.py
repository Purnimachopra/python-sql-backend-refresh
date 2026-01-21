from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user
from pydantic import BaseModel, EmailStr
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

# Pydantic schema for response
class UserRead(BaseModel):
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        orm_mode = True

# GET /users/me
@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }
