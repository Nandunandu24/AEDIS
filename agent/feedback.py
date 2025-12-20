from typing import List, Dict

def analyze_feedback(events: List[Dict]) -> Dict:
    """
    Analyze past agent events and generate feedback signals.
    """

    feedback = {
        "increase_caution": False,
        "decrease_caution": False,
        "notes": []
    }

    if not events:
        return feedback

    escalations = 0
    successes = 0

    for event in events:
        execution = event.get("execution_result", {})
        status = execution.get("status")

        if status == "success":
            successes += 1

        if event.get("action_plan", {}).get("action") == "escalate_to_human":
            escalations += 1

    escalation_rate = escalations / len(events)

    # --- Simple self-correction rules ---
    if escalation_rate > 0.7:
        feedback["increase_caution"] = True
        feedback["notes"].append(
            "High escalation rate detected. Reduce auto-resolution."
        )

    if escalation_rate < 0.3 and successes > 3:
        feedback["decrease_caution"] = True
        feedback["notes"].append(
            "Low escalation rate with successes. Safe to auto-resolve more."
        )

    return feedback
