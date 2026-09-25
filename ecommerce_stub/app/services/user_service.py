"""
user_service.py — Stub implementation of UserService.
All methods are placeholders; implementations are injected by the Spec2Code pipeline.
"""
from typing import Optional
from app.models.user import User, UserCreate, SessionToken


class UserService:
    """Handles user registration and authentication."""

    def register_user(self, data: UserCreate) -> User:
        """REQ-001: Register a new user with unique email."""
        pass

    def login(self, email: str, password: str) -> Optional[SessionToken]:
        """REQ-002: Authenticate user and return session token."""
        pass
