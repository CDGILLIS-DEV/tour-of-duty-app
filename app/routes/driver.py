from fastapi import APIRouter, Depends
from app.dependencies.auth import require_role
from app.schemas import UserRoles
from app.models import User

router = APIRouter

@router.get("/driver/dashboard")
def driver_dashboard(current_user: User = Depends(require_role(UserRoles.driver))):
    return {"message": f"Welcome {current_user.name}"}