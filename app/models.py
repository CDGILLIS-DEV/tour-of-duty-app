from sqlalchemy import Column, Date, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="driver") # 'driver' or 'admin'


class LoadLeg(Base):
    __tablename__ = "load_legs"

    id =  Column(Integer, primary_key=True, index=True)
    leg_number = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    origin = Column(String, nullable=False)
    origin_city_state = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    destination_city_state = Column(String, nullable=False)
    container_number = Column(String, nullable=False)
    chassis_number = Column(String, nullable=False)
    pro_number = Column(String, nullable=False)
    details = Column(String, nullable=False)
