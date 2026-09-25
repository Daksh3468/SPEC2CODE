"""
orders.py — FastAPI router for order endpoints.
"""
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.order import Order, OrderItem, OrderStatus
from app.services.order_service import OrderService

router = APIRouter()
_svc = OrderService()


@router.post("/", response_model=Order)
def place_order(user_id: str, items: List[OrderItem]):
    result = _svc.place_order(user_id, items)
    if result is None:
        raise HTTPException(status_code=400, detail="Could not place order")
    return result


@router.get("/{order_id}/status")
def get_order_status(order_id: str):
    status = _svc.get_order_status(order_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": order_id, "status": status}


@router.get("/history/{user_id}", response_model=List[Order])
def get_order_history(user_id: str, page: int = 1):
    return _svc.get_order_history(user_id, page) or []


@router.post("/{order_id}/cancel", response_model=Order)
def cancel_order(order_id: str):
    result = _svc.cancel_order(order_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return result


@router.post("/{order_id}/ship")
def update_shipping(order_id: str, tracking_number: str):
    result = _svc.update_shipping(order_id, tracking_number)
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return result
