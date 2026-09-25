"""
inventory_service_patch.py — Generated implementation of InventoryService.
Applied by Spec2Code Stage 3 (Code Generation Agent).
REQs covered: REQ-010, REQ-015, REQ-020
"""

LOW_STOCK_THRESHOLD = 10


class InventoryService:
    """Handles stock reservation, release, and low-stock alerting."""

    # In-memory inventory store: product_id → available count
    _stock: dict = {}
    # Reserved stock: product_id → reserved count
    _reserved: dict = {}

    def reserve_stock(self, product_id: str, quantity: int) -> dict:
        """REQ-010: Reserve stock for an ordered product."""
        available = self._stock.get(product_id, 100)  # Default 100 for demo
        if available < quantity:
            return {"success": False, "error": "Insufficient stock"}
        self._stock[product_id] = available - quantity
        self._reserved[product_id] = self._reserved.get(product_id, 0) + quantity
        return {
            "success": True,
            "product_id": product_id,
            "reserved": quantity,
            "remaining_available": self._stock[product_id],
        }

    def release_stock(self, product_id: str, quantity: int) -> dict:
        """REQ-015: Release reserved stock back to available when order is cancelled."""
        reserved = self._reserved.get(product_id, 0)
        release_qty = min(quantity, reserved)
        self._reserved[product_id] = reserved - release_qty
        self._stock[product_id] = self._stock.get(product_id, 0) + release_qty
        return {
            "success": True,
            "product_id": product_id,
            "released": release_qty,
            "available_now": self._stock[product_id],
        }

    def check_low_stock(self, product_id: str, current_stock: int) -> dict:
        """REQ-020: Trigger alert if stock drops below threshold."""
        is_low = current_stock < LOW_STOCK_THRESHOLD
        result = {
            "product_id": product_id,
            "current_stock": current_stock,
            "threshold": LOW_STOCK_THRESHOLD,
            "alert_triggered": is_low,
        }
        if is_low:
            print(f"  ⚠️  [ALERT] Low stock for {product_id}: {current_stock} units remaining")
        return result
