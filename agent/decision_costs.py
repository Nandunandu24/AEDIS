# agent/decision_costs.py

COST_MATRIX = {
    "auto_resolve_wrong": 50,      # customer churn, refunds, trust loss
    "escalate_unnecessary": 10,    # human effort cost
    "delay_decision": 20           # SLA / frustration cost
}
