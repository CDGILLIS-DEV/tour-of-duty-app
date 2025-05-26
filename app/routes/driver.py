from fastapi import APIRouter, Depends

from app.dependencies.auth import require_role, get_current_driver
from app.schemas import UserRoles
from app.models import User

router = APIRouter

@router.get("/driver/dashboard")
def driver_dashboard(current_user: User = Depends(require_role(UserRoles.driver))):
    # Logic to return dashboard for this driver
    return {"message": f"Welcome {current_user.name}"}

@router.get("/driver/load-legs")
def get_driver_legs(current_user: User =  Depends(get_current_driver)):
    # Logic to return legs for this driver
    return{"message": f"Hello, {current_user.name}. Here are your load legs."}