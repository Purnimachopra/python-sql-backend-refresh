from fastapi import APIRouter, Depends
from app.core.dependencies import admin_required

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard")
def dashboard(user=Depends(admin_required)):
    return {"message": f"Welcome admin {user.email}"}
