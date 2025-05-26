from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user, require_role, require_admin, verify_password, create_access_token
from app.utils import hash_password

router = APIRouter()

@router.get("/admin-only")
def admin_dashboard(current_user: models.User = Depends(require_admin)):
    return {"message": f"Welcome, {current_user.name}. You are an admin."}

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first(): # check if email already registered
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(
        id=user.id,
        name=user.name,
        email=user.email,
        hashed_password= hash_password(user.password),
        role=user.role
    )
    db.add(new_user) # put new user in db queue
    db.commit() # add new user to db
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def read_current_user(user=Depends(get_current_user)):
    return {"email": user["sub"], "role": user["role"]}

@router.get("/admin-only")
def admin_area(user=Depends(require_role("admin"))):
    return {"message": f"Welcome admin: {user['sub']}"}
