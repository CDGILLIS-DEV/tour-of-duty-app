from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./tourofduty.db"

engine =  create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    from app.models import Base
    Base.metadata.create_all(bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally: 
        db.close()