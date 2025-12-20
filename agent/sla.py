# agent/sla.py

from datetime import datetime, timedelta

# SLA limits per decision type
SLA_RULES = {
    "auto_resolve": timedelta(hours=24),
    "request_info": timedelta(hours=48),
    "escalate": timedelta(days=7),
}


def is_sla_breached(decision: str, created_at: str) -> bool:
    """
    Checks whether SLA is breached for a decision.
    """

    if not created_at or decision not in SLA_RULES:
        return False

    created_time = datetime.fromisoformat(created_at)
    now = datetime.utcnow()

    allowed_duration = SLA_RULES[decision]
    return (now - created_time) > allowed_duration
