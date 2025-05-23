from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "driver"

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        orm_mode = True

# Shared template
class LoadLegBase(BaseModel):
    leg_number: int
    date: date
    origin: str
    origin_city_state: str
    destination: str
    destination_city_state: str
    container_number: str
    chassis_number: str
    pro_number: str
    details: str

# For creation (input)
class LoadLegCreate(LoadLegBase):
    pass 

# For response (output)
class LoadLegResponse(LoadLegBase):
    id: int

    class Config:
        orm_mode = True




