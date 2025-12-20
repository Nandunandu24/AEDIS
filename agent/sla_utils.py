from datetime import datetime, timedelta, timezone
from agent.sla import SLA_RULES


def sla_status(decision: str, created_at: str):
    """
    Returns SLA status for a given decision.

    Args:
        decision (str): Decision type (must exist in SLA_RULES)
        created_at (str): ISO 8601 timestamp string

    Returns:
        dict | None
    """

    if not decision or decision not in SLA_RULES or not created_at:
        return None

    try:
        # Parse ISO time safely
        created_time = datetime.fromisoformat(created_at)

        # Make timezone-aware (assume UTC if missing)
        if created_time.tzinfo is None:
            created_time = created_time.replace(tzinfo=timezone.utc)

    except ValueError:
        return None

    deadline = created_time + SLA_RULES[decision]
    now = datetime.now(timezone.utc)

    remaining = deadline - now
    breached = remaining.total_seconds() <= 0

    return {
        "decision": decision,
        "created_at": created_time.isoformat(),
        "deadline": deadline.isoformat(),
        "remaining_seconds": max(0, int(remaining.total_seconds())),
        "breached": breached
    }
