"""
cart_service.py — Stub implementation of CartService.
All methods are placeholders; implementations are injected by the Spec2Code pipeline.
"""
from typing import List, Dict


class CartService:
    """Manages shopping cart state per user."""

    def add_item(self, user_id: str, product_id: str, quantity: int) -> dict:
        """REQ-005: Add a product to the user's cart."""
        pass

    def get_cart(self, user_id: str) -> dict:
        """REQ-006: Return cart contents with totals."""
        pass
