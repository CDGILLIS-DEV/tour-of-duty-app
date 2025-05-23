from pydantic import BaseModel, EmailStr, Field
from datetime import date
from enum import Enum

# Define user role
class UserRole(str, Enum):
    driver = "driver"
    admin = "admin"

# Shared template
class UserBase(BaseModel):
    id: int = Field(..., description="Driver ID (City Code + 3 Digit Truck Number, e.g., 3063XXX(Atlanta))")
    name: str = Field(..., description="Driver's full name")
    email: EmailStr = Field(description="Driver's email address")
    role: UserRole = Field(..., description="Role of the user (driver or admin)") # Ensures only "driver" or "admin" can be selected during registration

# For creation (input)
class UserCreate(UserBase):
    password: str = Field(..., description="Driver password")

class UserLogin(BaseModel):
    id_number: str = Field(..., description="Driver ID used for login")
    password: str = Field(..., description="Driver password")

class UserResponse(UserBase):
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




