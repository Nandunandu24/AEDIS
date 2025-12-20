from agent.agent_loop import run_agent


def test_auto_resolve_refund_within_7_days():
    result = run_agent(
        email_text="I requested a refund 3 days ago. Order ID: ORD-12345",
        meta={
            "length": 50,
            "has_attachment": False,
            "sentiment": 0.2,
            "past_interactions": 0
        }
    )
    assert result["decision"]["final_decision"] == "auto_resolve"
    assert result["customer_response"] is not None


def test_escalate_refund_over_7_days():
    result = run_agent(
        email_text="I requested a refund 10 days ago and still haven't received it.",
        meta={
            "length": 80,
            "has_attachment": False,
            "sentiment": -0.6,
            "past_interactions": 2
        }
    )
    assert result["decision"]["final_decision"] == "escalate"
    assert result["customer_response"] is None


def test_sentiment_changes_tone():
    positive = run_agent(
        email_text="Just checking my order status. Thanks!",
        meta={
            "length": 40,
            "has_attachment": False,
            "sentiment": 0.6,
            "past_interactions": 0
        }
    )

    negative = run_agent(
        email_text="Why is this taking so long?",
        meta={
            "length": 40,
            "has_attachment": False,
            "sentiment": -0.7,
            "past_interactions": 0
        }
    )

    assert "Thank you for reaching out" in positive["customer_response"]
    assert "We understand your frustration" in negative["customer_response"]
