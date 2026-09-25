"""
order.py — Order domain model for ShopFlow.
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"


class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    unit_price: float


class Order(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING
    transaction_id: Optional[str] = None
    tracking_number: Optional[str] = None
    refund_amount: Optional[float] = None
