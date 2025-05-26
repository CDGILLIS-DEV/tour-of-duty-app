from fastapi import Depends, HTTPException, status
from app.models import User
from app.auth import get_current_user

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to access this resource",            
        )
    return current_user