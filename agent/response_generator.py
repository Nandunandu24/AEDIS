# agent/response_generator.py
from typing import Optional


def generate_auto_reply(
    email_text: str,
    decision: str,
    sentiment: float,
    sla_breached: bool = False
) -> Optional[str]:
    """
    Generates a safe customer-facing reply.

    Rules:
    - SLA breached → send holding / reassurance reply
    - auto_resolve → send solution reply
    - request_info → ask clarification
    - escalate only → no reply unless SLA breached
    """

    email_lower = email_text.lower()

    # 🔴 SLA breached → ALWAYS reassure customer
    if sla_breached:
        return (
            "Thank you for reaching out to us.\n\n"
            "We understand the urgency of your request. Your case has been "
            "escalated to our support team and is currently under review.\n\n"
            "You can expect an update shortly. We appreciate your patience."
        )

    # ✅ AUTO RESOLVE RESPONSES
    if decision == "auto_resolve":

        if "refund" in email_lower:
            return (
                "✅ Your refund request has been received and is being processed.\n\n"
                "Refunds are usually completed within 5–7 business days. "
                "You will be notified once the refund is issued.\n\n"
                "Thank you for your patience."
            )

        if "cancel" in email_lower or "subscription" in email_lower:
            return (
                "✅ Your subscription cancellation request has been processed.\n\n"
                "No further charges will be applied. "
                "Please let us know if you need any further assistance."
            )

        if "delay" in email_lower or "status" in email_lower:
            return (
                "📦 Your order is currently being processed and is within the "
                "expected delivery timeline.\n\n"
                "We will notify you if there are any updates."
            )

        return (
            "Thank you for contacting us.\n\n"
            "Your request has been reviewed and handled successfully. "
            "Please feel free to reply if you need further assistance."
        )

    # ℹ️ REQUEST INFO
    if decision == "request_info":
        return (
            "Thank you for contacting us.\n\n"
            "To proceed with your request, could you please share:\n"
            "- Order ID\n"
            "- Date of purchase or refund request\n\n"
            "Once we receive this information, we will resolve your issue promptly."
        )

    # ❌ No reply for pure escalation without SLA breach
    return None
