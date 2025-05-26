from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models import User
from app.schemas import UserLogin, Token
from app.utils import verify_password
from app.dependencies.auth import create_access_token

