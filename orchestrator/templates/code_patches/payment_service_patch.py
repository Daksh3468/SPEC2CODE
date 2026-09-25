"""
payment_service_patch.py — Generated implementation of PaymentService.
Applied by Spec2Code Stage 3 (Code Generation Agent).
REQs covered: REQ-009, REQ-014
"""
import uuid
from typing import Optional


class PaymentService:
    """Handles payment charging and refunds."""

    # In-memory transaction store for demo
    _transactions: dict = {}

    def charge_payment(self, user_id: str, amount: float, payment_method: str) -> dict:
        """REQ-009: Charge payment method and return transaction record."""
        transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
        record = {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "amount": round(amount, 2),
            "payment_method": payment_method,
            "status": "CHARGED",
        }
        self._transactions[transaction_id] = record
        return record

    def refund_payment(self, transaction_id: str, amount: float) -> dict:
        """REQ-014: Issue full refund for a cancelled order."""
        original = self._transactions.get(transaction_id)
        if original is None:
            return {"success": False, "error": "Transaction not found"}
        refund_id = f"REF-{uuid.uuid4().hex[:8].upper()}"
        refund = {
            "refund_id": refund_id,
            "original_transaction_id": transaction_id,
            "amount": round(amount, 2),
            "status": "REFUNDED",
        }
        original["status"] = "REFUNDED"
        self._transactions[transaction_id] = original
        return refund
