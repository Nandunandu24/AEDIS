from typing import Dict, List

def generate_explanation(
    email_text: str,
    decision_output: Dict,
    action_plan: Dict,
    feedback: Dict
) -> str:
    """
    Generate a safe, deterministic explanation for agent behavior.
    (No LLM yet – rule-based explanation)
    """

    decision = decision_output.get("final_decision")
    policies = decision_output.get("policies_used", [])
    confidence = decision_output.get("ml_output", {}).get("confidence", 0.0)

    explanation_parts = []

    # --- Decision explanation ---
    explanation_parts.append(
        f"The system classified this email with a confidence score of {confidence:.2f}."
    )

    if policies:
        explanation_parts.append(
            "The following policies were relevant to this decision:"
        )
        for p in policies:
            explanation_parts.append(f"- {p}")

    # --- Action explanation ---
    action = action_plan.get("action")

    if action == "escalate_to_human":
        explanation_parts.append(
            "The issue was escalated to human support to reduce risk and ensure policy compliance."
        )

    elif action == "send_auto_reply":
        explanation_parts.append(
            "The issue was auto-resolved because it was low-risk and met confidence thresholds."
        )

    elif action == "request_additional_information":
        explanation_parts.append(
            "Additional information was requested because required details were missing."
        )

    # --- Feedback explanation ---
    if feedback.get("increase_caution"):
        explanation_parts.append(
            "Recent historical outcomes caused the system to behave more cautiously."
        )

    if feedback.get("decrease_caution"):
        explanation_parts.append(
            "Recent successful outcomes allowed the system to be less conservative."
        )

    return " ".join(explanation_parts)
