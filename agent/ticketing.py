import uuid
from datetime import datetime
from typing import Dict


def create_escalation_ticket(
    email_text: str,
    decision_output: Dict
) -> Dict:
    """
    Mock Jira ticket creation.
    """

    ticket = {
        "ticket_id": f"JIRA-{uuid.uuid4().hex[:6].upper()}",
        "created_at": datetime.utcnow().isoformat(),
        "priority": "HIGH" if decision_output["ml_output"]["confidence"] < 0.6 else "MEDIUM",
        "status": "OPEN",
        "summary": decision_output["final_decision"],
        "description": email_text
    }

    # In real system → POST to Jira REST API
    return ticket
