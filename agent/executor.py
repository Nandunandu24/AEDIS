from typing import Dict
from datetime import datetime

def execute_action(action_plan: Dict) -> Dict:
    """
    Executes the agent action plan safely (simulation).
    """

    action = action_plan["action"]
    steps = action_plan.get("steps", [])

    outcome = {
        "action": action,
        "status": "pending",
        "executed_steps": [],
        "timestamp": datetime.utcnow().isoformat()
    }

    # -----------------------------
    # EXECUTION LOGIC (SIMULATED)
    # -----------------------------
    if action == "send_auto_reply":
        outcome["status"] = "success"
        outcome["executed_steps"] = steps

    elif action == "escalate_to_human":
        outcome["status"] = "success"
        outcome["executed_steps"] = steps

    elif action == "request_additional_information":
        outcome["status"] = "success"
        outcome["executed_steps"] = steps

    elif action == "delay_decision":
        outcome["status"] = "delayed"
        outcome["executed_steps"] = steps

    else:
        outcome["status"] = "manual_intervention_required"
        outcome["executed_steps"] = steps

    return outcome
