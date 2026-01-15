#Role-Protected Routes

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
def admin_dashboard(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise PermissionError("Admin access required")

    return {"message": "Welcome Admin"}
