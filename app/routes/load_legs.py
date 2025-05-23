from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import LoadLegCreate, LoadLegResponse
from app.database import SessionLocal, get_db
from app.models import LoadLeg
from typing import List
from datetime import date


router = APIRouter()

@router.post("/load-legs/", response_model=LoadLegResponse)
def create_load_leg(load_leg: LoadLegCreate, db: Session = Depends(get_db)):
    db_load_leg = LoadLeg(**load_leg.model_dump())
    db.add(db_load_leg)
    db.commit()
    db.refresh(db_load_leg)
    return db_load_leg

@router.get("/load-leg/", response_model=list[LoadLegResponse])
def get_all_load_legs(db: Session = Depends(get_db)):
    return db.query(LoadLeg).all()

@router.get("/legs/{leg_date}", response_model=List[LoadLegResponse])
def get_legs_by_date(leg_date: date, db: Session = Depends(get_db)):
    legs = db.query(LoadLeg).filter(LoadLeg.date == leg_date).all()
    if not legs:
        raise HTTPException(status_code=404, detail="No legs found for this date")
    return legs
