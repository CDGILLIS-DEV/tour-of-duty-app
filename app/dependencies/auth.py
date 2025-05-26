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
        status_code=status.HTTP_401_UNAUTHORIZED,
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

def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRoles.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Admin access required",
                            )
    return current_user

def get_current_driver(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRoles.driver:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Driver access required", 
                            )
    return current_user



