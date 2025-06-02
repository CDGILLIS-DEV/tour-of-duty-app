from sqlalchemy import Column, Integer, String, Date, Enum as SqlEnum
from app.dependencies.db import Base
from app.schemas import UserRoles
import enum



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    id_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(UserRoles), nullable=False,) # 'driver' or 'admin'


class LoadLeg(Base):
    __tablename__ = "load_legs"

    id =  Column(Integer, primary_key=True, index=True)
    truck_number = Column(Integer, nullable=False)
    truck_owner = Column(String, nullable=True)
    driver_name = Column(String, nullable=False, default=User.name)
    date = Column(Date, nullable=False)
    leg_number = Column(Integer, nullable=False)
    origin_city_state = Column(String, nullable=False)
    origin_customer = Column(String, nullable=False)
    destination_city_state = Column(String, nullable=False)
    destination_customer = Column(String, nullable=False)
    container_number = Column(String, nullable=False)
    chassis_number = Column(String, nullable=False)
    pro_number = Column(String, nullable=False)
    load_details = Column(String, nullable=False)
    beg_odometer_reading = Column(Integer, nullable=False)
    end_odometer_reading = Column(Integer, nullable=False)
