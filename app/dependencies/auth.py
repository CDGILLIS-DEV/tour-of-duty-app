from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.models import User
from app.dependencies.db import get_db
from app.schemas import UserRoles
from app.utils import verify_password, get_password_hash, create_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)




def get_current_user(token: str = Depends(api_key_header)):
    if not token.startswith("Bearer " ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"    
        )
    token_value = token.split(" ")[1] # Proceed to decode and validate JWT

def require_role(required_role: UserRoles):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {require_role} role"   
            )
        return user
    return role_checker

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to access this resource",            
        )
    return current_user