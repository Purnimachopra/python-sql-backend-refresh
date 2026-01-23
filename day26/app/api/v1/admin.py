from fastapi import APIRouter, Depends
from app.api.deps import require_admin
from app.models.user import User
router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard")
def admin_dashboard(admin: User = Depends(require_admin)):
    return {
        "message": f"Welcome admin {admin.email}",
        "role": admin.role,
    }
