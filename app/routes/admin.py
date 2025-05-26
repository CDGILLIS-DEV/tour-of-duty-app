from fastapi import APIRouter, Depends
from app.dependencies.auth import require_role
from app.schemas import UserRoles
from app.models import User

router = APIRouter

@router.get("/admin/dashboard")
def admin_dashboard(current_user: User = Depends(require_role(UserRoles.admin))):
    return {"message": f"Welcome admin {current_user.name}!"}