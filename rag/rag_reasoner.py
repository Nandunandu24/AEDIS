from typing import Dict, List
import re


# -----------------------------
# Helpers
# -----------------------------

def _extract_days(text: str) -> int:
    """
    Extract number of days mentioned in email text.
    Example: 'refund 3 days ago' → 3
    """
    match = re.search(r"(\d+)\s+day", text.lower())
    return int(match.group(1)) if match else -1


def _is_refund_request(text: str) -> bool:
    return "refund" in text.lower()


def _generate_auto_reply(sentiment: float) -> str:
    """
    Tone-aware auto response (used ONLY for auto_resolve)
    """
    if sentiment >= 0.3:
        return (
            "Thank you for reaching out! 😊\n\n"
            "Your request has been received and is being processed. "
            "Please rest assured that we are actively looking into it."
        )

    if sentiment >= -0.3:
        return (
            "Thank you for contacting us.\n\n"
            "We have received your request and are currently checking the details. "
            "We’ll update you shortly."
        )

    return (
        "We understand your concern and apologize for the delay.\n\n"
        "Your request has been noted, and we are working to resolve this as quickly as possible."
    )


# -----------------------------
# Core Reasoner
# -----------------------------

def reason_with_policy(email_text: str, meta: Dict) -> Dict:
    """
    Core decision intelligence logic:
    Policy > SLA > Cost > ML > Sentiment
    """

    sentiment = meta.get("sentiment", 0.0)
    past_interactions = meta.get("past_interactions", 0)

    policies_used: List[str] = []
    customer_response = None

    # =====================================================
    # HARD POLICY: REFUND RULES (NON-OVERRIDABLE)
    # =====================================================
    if _is_refund_request(email_text):
        days = _extract_days(email_text)

        # 🔴 HARD ESCALATION RULE
        if days != -1 and days > 7:
            policies_used.append(
                "POLICY: Refund requests older than 7 days must be escalated."
            )

            return {
                "final_decision": "escalate",
                "ml_output": {
                    "predicted_label": "escalate",
                    "risk_score": 1.0,
                    "confidence": 1.0,
                },
                "policies_used": policies_used,
                "customer_response": None,
            }

        # 🟢 SAFE AUTO-RESOLVE
        if days != -1 and days <= 7:
            policies_used.append(
                "POLICY: Refund requests within 7 days can be auto-resolved."
            )
            customer_response = _generate_auto_reply(sentiment)

            return {
                "final_decision": "auto_resolve",
                "ml_output": {
                    "predicted_label": "auto_resolve",
                    "risk_score": 0.2,
                    "confidence": 0.85,
                },
                "policies_used": policies_used,
                "customer_response": customer_response,
            }

        # Refund mentioned but days missing → request info
        policies_used.append(
            "POLICY: Refund request missing timeline — request clarification."
        )

        return {
            "final_decision": "request_info",
            "ml_output": {
                "predicted_label": "request_info",
                "risk_score": 0.6,
                "confidence": 0.6,
            },
            "policies_used": policies_used,
            "customer_response": None,
        }

    # =====================================================
    # LOW-RISK GENERAL QUERIES
    # =====================================================
    if sentiment > -0.8 and past_interactions < 3:
        policies_used.append(
            "POLICY: Low-risk informational queries can be auto-resolved."
        )
        customer_response = _generate_auto_reply(sentiment)

        return {
            "final_decision": "auto_resolve",
            "ml_output": {
                "predicted_label": "auto_resolve",
                "risk_score": 0.2,
                "confidence": 0.8,
            },
            "policies_used": policies_used,
            "customer_response": customer_response,
        }

    # =====================================================
    # FALLBACK
    # =====================================================
    policies_used.append(
        "POLICY: Insufficient information or high risk — request clarification."
    )

    return {
        "final_decision": "request_info",
        "ml_output": {
            "predicted_label": "request_info",
            "risk_score": 0.7,
            "confidence": 0.7,
        },
        "policies_used": policies_used,
        "customer_response": None,
    }
