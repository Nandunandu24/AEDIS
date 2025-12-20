# agent/cost_engine.py

from typing import Dict
from agent.decision_costs import COST_MATRIX


def choose_action_by_cost(confidence: float) -> str:
    """
    Chooses the action that minimizes expected business cost.

    Args:
        confidence (float): Model confidence (0.0 – 1.0)

    Returns:
        str: Selected action
    """

    confidence = _sanitize_confidence(confidence)

    costs = _compute_costs(confidence)

    # Select action with minimum expected cost
    return min(costs, key=costs.get)


def cost_breakdown(confidence: float) -> Dict[str, float]:
    """
    Returns detailed cost breakdown for transparency & UI display.
    """

    confidence = _sanitize_confidence(confidence)

    costs = _compute_costs(confidence)

    # Round only for presentation
    return {k: round(v, 2) for k, v in costs.items()}


# ----------------- Internal helpers -----------------

def _compute_costs(confidence: float) -> Dict[str, float]:
    """
    Core expected cost computation logic.
    """

    return {
        "auto_resolve": (1 - confidence) * COST_MATRIX["auto_resolve_wrong"],
        "escalate": COST_MATRIX["escalate_unnecessary"],
        "request_info": COST_MATRIX["delay_decision"],
    }


def _sanitize_confidence(confidence: float) -> float:
    """
    Ensures confidence is within valid bounds.
    """

    if confidence is None:
        return 0.0

    return max(0.0, min(1.0, float(confidence)))
