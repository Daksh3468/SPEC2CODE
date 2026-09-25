"""
product_service.py — Stub implementation of ProductService.
All methods are placeholders; implementations are injected by the Spec2Code pipeline.
"""
from typing import Optional
from app.models.product import Product, ProductPage


class ProductService:
    """Handles product listing, detail, and search."""

    def list_products(self, page: int = 1, page_size: int = 20) -> ProductPage:
        """REQ-003: Return paginated product list."""
        pass

    def get_product(self, product_id: str) -> Optional[Product]:
        """REQ-004: Return full product details."""
        pass

    def search_products(self, keyword: str, page: int = 1) -> ProductPage:
        """REQ-018: Search products by keyword."""
        pass
