"""
user.py — User domain model for ShopFlow.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    user_id: str
    email: str
    full_name: str
    hashed_password: str
    is_active: bool = True


class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class SessionToken(BaseModel):
    user_id: str
    token: str
