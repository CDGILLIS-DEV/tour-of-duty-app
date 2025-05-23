from fastapi import FastAPI
from app.database import engine, create_db_and_tables
from app.models import Base
from app.routes import users
from app.routes import load_legs

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(load_legs.router)
create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Tour of Duty API is live!"}