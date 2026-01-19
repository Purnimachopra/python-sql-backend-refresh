from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/users", tags=["users"])

# Pydantic schema for response
class UserRead(BaseModel):
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        orm_mode = True

# GET /users/me
@router.get("/me", response_model=UserRead)
def read_current_user(user=Depends(get_current_user)):
    """
    Returns information about the current logged-in user
    """
    return user
