def apply_human_override(original_decision: dict, override: str) -> dict:
    """
    Allows human to override agent decision
    """
    original_decision["final_decision"] = override
    original_decision["override_applied"] = True
    return original_decision
