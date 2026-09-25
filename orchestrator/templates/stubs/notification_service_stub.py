"""
notification_service.py — Stub implementation of NotificationService.
All methods are placeholders; implementations are injected by the Spec2Code pipeline.
"""


class NotificationService:
    """Handles transactional email notifications to customers."""

    def send_order_confirmation(self, user_email: str, order_id: str, total_amount: float) -> dict:
        """REQ-008: Send confirmation email after successful order placement."""
        pass

    def send_cancellation_email(self, user_email: str, order_id: str, refund_amount: float) -> dict:
        """REQ-017: Send cancellation confirmation email including order ID and refund amount."""
        pass
