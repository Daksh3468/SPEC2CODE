"""
notification_service_patch.py — Generated implementation of NotificationService.
Applied by Spec2Code Stage 7 (Auto-Fix Agent) for REQ-017.
REQs covered: REQ-008, REQ-017
"""


class NotificationService:
    """Handles transactional email notifications to customers."""

    def send_order_confirmation(self, user_email: str, order_id: str, total_amount: float) -> dict:
        """REQ-008: Send confirmation email after successful order placement."""
        # Simulate sending email (demo: logs and returns confirmation record)
        print(f"  📧 [EMAIL] Order confirmation → {user_email} | Order: {order_id} | Total: ${total_amount:.2f}")
        return {
            "sent": True,
            "type": "order_confirmation",
            "recipient": user_email,
            "order_id": order_id,
            "total_amount": total_amount,
        }

    def send_cancellation_email(self, user_email: str, order_id: str, refund_amount: float) -> dict:
        """REQ-017: Send cancellation confirmation email including order ID and refund amount."""
        # Simulate sending email (demo: logs and returns confirmation record)
        print(f"  📧 [EMAIL] Cancellation confirmation → {user_email} | Order: {order_id} | Refund: ${refund_amount:.2f}")
        return {
            "sent": True,
            "type": "cancellation_confirmation",
            "recipient": user_email,
            "order_id": order_id,
            "refund_amount": refund_amount,
        }
