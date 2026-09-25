"""
product.py — Product domain model for ShopFlow.
"""
from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    product_id: str
    name: str
    description: str
    price: float
    stock_count: int
    images: List[str] = []
    is_available: bool = True


class ProductPage(BaseModel):
    items: List[Product]
    total: int
    page: int
    page_size: int
