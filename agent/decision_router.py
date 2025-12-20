from typing import Dict


def route_decision(decision: Dict) -> str:
    """
    Routes a decision based on confidence and decision type.

    Returns:
        AUTO_EXECUTE
        HUMAN_REVIEW
        BLOCK
    """

    final_decision = decision.get("final_decision")
    ml_output = decision.get("ml_output", {})
    confidence = ml_output.get("confidence", 0.0)

    # Hard blocks (never auto execute)
    if final_decision in {"escalate", "block"}:
        return "HUMAN_REVIEW"

    # Auto-resolve cases
    if final_decision == "auto_resolve":
        if confidence >= 0.8:
            return "AUTO_EXECUTE"
        elif confidence >= 0.6:
            return "HUMAN_REVIEW"
        else:
            return "BLOCK"

    # Fallback
    return "HUMAN_REVIEW"
