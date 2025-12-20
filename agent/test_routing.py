from agent.decision_router import route_decision

def test_high_confidence_auto_exec():
    decision = {
        "final_decision": "auto_resolve",
        "ml_output": {"confidence": 0.9}
    }
    assert route_decision(decision) == "AUTO_EXECUTE"


def test_medium_confidence_human_review():
    decision = {
        "final_decision": "auto_resolve",
        "ml_output": {"confidence": 0.65}
    }
    assert route_decision(decision) == "HUMAN_REVIEW"
