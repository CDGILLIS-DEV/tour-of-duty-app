from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user
from app.models import User
from app.schemas import UserRoles

def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to access this resource",            
        )
    return user

def require_driver(user: User = Depends(get_current_user)):
    if user.role != UserRoles.driver:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to drivers."
        )
    return user

def require_role(required_role: UserRoles):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {require_role} role"   
            )
        return user
    return role_checker