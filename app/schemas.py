from pydantic import BaseModel, EmailStr, Field
from datetime import date
from enum import Enum


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type, usually 'bearer'")

# Define user role
class UserRoles(str, Enum):
    driver = "driver"
    admin = "admin"

# Shared template
class UserBase(BaseModel):
    id: int = Field(..., description="Driver ID (City Code + 3 Digit Truck Number, e.g., 3063XXX(Atlanta))")
    name: str = Field(..., description="Driver's full name")
    email: EmailStr = Field(description="Driver's email address")
    role: UserRoles = Field(..., description="Role of the user (driver or admin)") # Ensures only "driver" or "admin" can be selected during registration

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
    truck_number: int
    truck_owner: str
    driver_name: str
    date: date
    leg_number: int
    origin_city_state: str
    origin_customer: str
    destination_city_state: str
    destination_customer: str
    container_number: str
    chassis_number: str
    pro_number: str
    load_details: str
    beg_odometer_reading: int
    end_odometer_reading: int

# For creation (input)
class LoadLegCreate(LoadLegBase):
    pass 

# For response (output)
class LoadLegResponse(LoadLegBase):
    id: int

    class Config:
        orm_mode = True




