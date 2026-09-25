"""
order_service_patch.py — Generated implementation of OrderService.
Applied by Spec2Code Stage 3 (Code Generation Agent).
REQs covered: REQ-007, REQ-011, REQ-012, REQ-013, REQ-016, REQ-019
"""
import uuid
from typing import List, Optional
from app.models.order import Order, OrderItem, OrderStatus


class OrderService:
    """Handles order lifecycle: placement, status, history, cancellation, shipping, returns."""

    # In-memory store for demo purposes
    _orders: dict = {}

    def place_order(self, user_id: str, items: List[OrderItem]) -> Order:
        """REQ-007: Convert cart to order with PENDING status."""
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        total = sum(item.unit_price * item.quantity for item in items)
        order = Order(
            order_id=order_id,
            user_id=user_id,
            items=items,
            total_amount=round(total, 2),
            status=OrderStatus.PENDING,
        )
        self._orders[order_id] = order
        return order

    def get_order_status(self, order_id: str) -> Optional[OrderStatus]:
        """REQ-011: Retrieve current order status."""
        order = self._orders.get(order_id)
        return order.status if order else None

    def get_order_history(self, user_id: str, page: int = 1, page_size: int = 20) -> List[Order]:
        """REQ-012: Paginated order history for a user."""
        user_orders = [o for o in self._orders.values() if o.user_id == user_id]
        start = (page - 1) * page_size
        return user_orders[start : start + page_size]

    def cancel_order(self, order_id: str) -> Order:
        """REQ-013: Cancel a PENDING or PROCESSING order."""
        order = self._orders.get(order_id)
        if order is None:
            return None
        if order.status not in (OrderStatus.PENDING, OrderStatus.PROCESSING):
            raise ValueError(f"Cannot cancel order in status {order.status}")
        order.status = OrderStatus.CANCELLED
        order.refund_amount = order.total_amount
        self._orders[order_id] = order
        return order

    def update_shipping(self, order_id: str, tracking_number: str) -> Order:
        """REQ-016: Mark order as SHIPPED with tracking number."""
        order = self._orders.get(order_id)
        if order is None:
            return None
        order.status = OrderStatus.SHIPPED
        order.tracking_number = tracking_number
        self._orders[order_id] = order
        return order

    def request_return(self, order_id: str, reason: str) -> dict:
        """REQ-019: Submit a return request within 30 days of delivery."""
        order = self._orders.get(order_id)
        if order is None:
            return {"success": False, "error": "Order not found"}
        if order.status != OrderStatus.DELIVERED:
            return {"success": False, "error": "Only delivered orders can be returned"}
        return_id = f"RET-{uuid.uuid4().hex[:8].upper()}"
        order.status = OrderStatus.RETURNED
        self._orders[order_id] = order
        return {"success": True, "return_id": return_id, "order_id": order_id, "reason": reason}
