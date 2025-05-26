from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.models import User
from app.dependencies.db import get_db
from app.schemas import UserRoles
from app.utils import verify_password, get_password_hash, create_access_token
from app.config import SECRET_KEY, ALGORITHM


api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

def get_current_user(
    token: str = Security(api_key_header),
    db: Session = Depends(get_db)
) -> User:
    credentials_exeption = HTTPException(
        status_code=401,
        detail="Invalid or missing credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token=SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id in None:
            raise credentials_exeption
    except JWTError:
        raise credentials_exeption
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exeption
    
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

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to access this resource",            
        )
    return current_user