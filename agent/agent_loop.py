# agent/agent_loop.py
from typing import Dict

# Core reasoning
from rag.rag_reasoner import reason_with_policy

# Agent components
from agent.planner import plan_action
from agent.executor import execute_action
from agent.memory import store_event, load_events
from agent.feedback import analyze_feedback
from agent.explainer import generate_explanation
from agent.decision_router import route_decision
from agent.response_generator import generate_auto_reply

# Cost + SLA
from agent.cost_engine import choose_action_by_cost
from agent.sla_utils import sla_status


def run_agent(email_text: str, meta: Dict) -> Dict:
    """
    Full autonomous agent loop:
    Observe → Policy → SLA → Cost → Route → Execute → Respond → Explain → Store
    """

    # --------------------------------------------------
    # 1️⃣ Load memory + feedback
    # --------------------------------------------------
    past_events = load_events(limit=20)
    feedback = analyze_feedback(past_events)

    # --------------------------------------------------
    # 2️⃣ POLICY REASONING (NON-OVERRIDABLE)
    # --------------------------------------------------
    decision_output = reason_with_policy(email_text, meta)
    final_decision = decision_output["final_decision"]
    confidence = decision_output["ml_output"]["confidence"]

    decision_output["decision_basis"] = "policy"

    # --------------------------------------------------
    # 3️⃣ SLA ENFORCEMENT (CAN OVERRIDE)
    # --------------------------------------------------
    created_at = meta.get("created_at")
    sla_breached =sla_status(final_decision, created_at)

    if sla_breached:
        final_decision = "escalate"
        decision_output["decision_basis"] = "sla_enforced"
        decision_output.setdefault("policies_used", []).append(
            "SLA breach escalation"
        )

    # --------------------------------------------------
    # 4️⃣ COST OPTIMIZATION (SAFE DOWNGRADE ONLY)
    # --------------------------------------------------
    elif final_decision == "auto_resolve":
        cost_decision = choose_action_by_cost(confidence)
        if cost_decision != "escalate":
            final_decision = cost_decision
            decision_output["decision_basis"] = "cost_optimization"

    decision_output["final_decision"] = final_decision

    # --------------------------------------------------
    # 5️⃣ ROUTING
    # --------------------------------------------------
    route = route_decision(decision_output)

    # --------------------------------------------------
    # 6️⃣ EXECUTION
    # --------------------------------------------------
    if route == "AUTO_EXECUTE":
        action_plan = plan_action(decision_output, feedback)
        execution_result = execute_action(action_plan)

    elif route == "HUMAN_REVIEW":
        action_plan = {
            "action": "await_human_review",
            "steps": ["Create review ticket"],
            "confidence": confidence
        }
        execution_result = {"status": "pending_human_review"}

    else:  # ESCALATE
        action_plan = plan_action(decision_output, feedback)
        execution_result = execute_action(action_plan)

    # --------------------------------------------------
    # 7️⃣ CUSTOMER RESPONSE (IMPORTANT FIX)
    # --------------------------------------------------
    customer_response = generate_auto_reply(
        email_text=email_text,
        decision=final_decision,
        sentiment=meta.get("sentiment", 0.0),
        sla_breached=sla_breached
    )

    # --------------------------------------------------
    # 8️⃣ EXPLANATION
    # --------------------------------------------------
    explanation = generate_explanation(
        email_text=email_text,
        decision_output=decision_output,
        action_plan=action_plan,
        feedback=feedback
    )

    # --------------------------------------------------
    # 9️⃣ STORE EVENT (AUDIT-READY)
    # --------------------------------------------------
    store_event({
        "email_text": email_text,
        "decision": decision_output,
        "route": route,
        "action_plan": action_plan,
        "execution_result": execution_result,
        "feedback_used": feedback,
        "explanation": explanation,
        "customer_response": customer_response,
        "meta": meta
    })

    # --------------------------------------------------
    # 🔟 RETURN
    # --------------------------------------------------
    return {
        "decision": decision_output,
        "route": route,
        "action_plan": action_plan,
        "execution_result": execution_result,
        "feedback": feedback,
        "explanation": explanation,
        "customer_response": customer_response
    }
