from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app.dependencies.db import get_db
from app.models import User
from app.schemas import UserLogin, Token
from app.utils import verify_password, create_access_token

router = APIRouter(prefix="/login", tags=["Authentication"])

@router.post("/", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_credentials.id_number).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid ID or password"
        )

    token_data = {
        "sub": str(user.id),
        "role": user.role
    }

    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }    




