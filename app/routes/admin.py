from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth import require_role, get_current_admin
from app.schemas import UserRoles
from app.models import User

router = APIRouter

@router.get("/admin/dashboard")
def admin_dashboard(current_user: User = Depends(require_role(UserRoles.admin))):
    return {"message": f"Welcome admin {current_user.name}!"}

@router.get("/admin/users")
def list_all_users(current_user: User = Depends(get_current_admin)):
    # Logic to return a list of users
    return {"message": f"Hi, admin {current_user.name}. Here are all users"}