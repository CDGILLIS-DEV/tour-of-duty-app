from fastapi import  APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.schemas import LoadLegCreate, LoadLegResponse, UserResponse
from app.dependencies.role_permissions import require_driver, require_admin
from app.dependencies.db import get_db
from app.models import LoadLeg, User, UserRoles
from app.dependencies.auth import get_current_user



router = APIRouter()

@router.post("/load-legs/", response_model=LoadLegResponse)
def create_load_leg(load_leg: LoadLegCreate, db: Session = Depends(get_db), user: UserResponse = Depends(get_current_user)):
    if user.role != UserRoles.driver:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only drivers can create legs.")
    
    db_load_leg = LoadLeg(**load_leg.model_dump())
    db.add(db_load_leg)
    db.commit()
    db.refresh(db_load_leg)
    return db_load_leg

@router.get("/admin/load-legs/", response_model=List[LoadLegResponse])
def get_all_legs(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(LoadLeg).all()

@router.get("/admin/load-legs/{leg_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_leg(leg_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    leg = db.query(LoadLeg).filter(LoadLeg.id == leg_id).first()
    if not leg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Load leg not found")
    db.delete(leg)
    db.commit()
    return

@router.put("/admin/load-leg/{leg_id}", response_model=LoadLegResponse)
def update_leg(leg_id: int, update_leg: LoadLegCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    leg = db.query(LoadLeg).filter(LoadLeg.id == leg_id).first()
    if not leg:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Load leg not found")
    
    for key, value in update_leg.model_dump().items():
        setattr(leg, key, value)
    
    db.commit()
    db.refresh(leg)
    return leg

@router.get("/admin/load-legs/by-driver/{driver_name}", response_model=List[LoadLegResponse])
def get_legs_by_driver(driver_name: str, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    legs = db.query(LoadLeg).filter(LoadLeg.driver_name == driver_name).all()
    if not legs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No legs found for this driver")
    return legs

@router.get("/load-leg/", response_model=list[LoadLegResponse])
def get_driver_legs(
    db: Session = Depends(get_db),
    user = Depends(require_driver)
):
    return db.query(LoadLeg).all()

@router.get("/legs/{leg_date}", response_model=List[LoadLegResponse])
def get_legs_by_date(
    leg_date: date,
    db: Session = Depends(get_db),
    user = Depends(require_driver)
):
    legs = db.query(LoadLeg).filter(LoadLeg.date == leg_date).all()
    if not legs:
        raise HTTPException(status_code=404, detail="No legs found for this date")
    return legs
