"""
users.py — FastAPI router for user endpoints.
"""
from fastapi import APIRouter, HTTPException
from app.models.user import User, UserCreate, UserLogin, SessionToken
from app.services.user_service import UserService

router = APIRouter()
_svc = UserService()


@router.post("/register", response_model=User)
def register_user(data: UserCreate):
    result = _svc.register_user(data)
    if result is None:
        raise HTTPException(status_code=400, detail="Registration failed")
    return result


@router.post("/login", response_model=SessionToken)
def login(data: UserLogin):
    result = _svc.login(data.email, data.password)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return result
