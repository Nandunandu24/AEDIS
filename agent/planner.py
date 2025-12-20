from typing import Dict


def plan_action(decision_payload: Dict, feedback: Dict = None) -> Dict:
    """
    Converts a decision into an executable action plan.
    Enables safe auto-resolution with feedback-based adaptation.
    """

    if feedback is None:
        feedback = {}

    decision = decision_payload.get("final_decision")
    ml_output = decision_payload.get("ml_output", {})
    confidence = ml_output.get("confidence", 0.0)

    # -----------------------------
    # ADAPTIVE CONFIDENCE THRESHOLD
    # -----------------------------
    base_threshold = 0.7

    if feedback.get("increase_caution"):
        threshold = 0.8   # slightly cautious, not blocking
    elif feedback.get("decrease_caution"):
        threshold = 0.6
    else:
        threshold = base_threshold

    # -----------------------------
    # ACTION PLAN STRUCTURE
    # -----------------------------
    plan = {
        "action": None,
        "steps": [],
        "confidence": confidence,
        "threshold_used": threshold
    }

    # -----------------------------
    # PLANNING LOGIC (FIXED)
    # -----------------------------

    # ✅ SAFE AUTO-RESOLVE
    if decision == "auto_resolve" and confidence >= threshold and not feedback.get("force_escalation"):
        plan["action"] = "send_auto_reply"
        plan["steps"] = [
            "Generate safe response",
            "Send reply to user",
            "Log resolution"
        ]

    # 🔴 ESCALATION (HARD STOP)
    elif decision == "escalate":
        plan["action"] = "escalate_to_human"
        plan["steps"] = [
            "Attach conversation history",
            "Notify support team",
            "Mark ticket as escalated"
        ]

    # 🟡 REQUEST MORE INFO
    elif decision == "request_info":
        plan["action"] = "request_additional_information"
        plan["steps"] = [
            "Identify missing fields",
            "Ask follow-up questions",
            "Wait for response"
        ]

    # ⏳ DELAY
    elif decision == "delay":
        plan["action"] = "delay_decision"
        plan["steps"] = [
            "Wait for more context",
            "Re-evaluate later"
        ]

    # ⚠️ FALLBACK
    else:
        plan["action"] = "manual_review"
        plan["steps"] = [
            "Fallback to human review"
        ]

    return plan
