from agent.agent_loop import run_agent

if __name__ == "__main__":
    result = run_agent(
        email_text="Refund not received for 10 days",
        meta={
            "length": 30,
            "has_attachment": False,
            "sentiment": -0.7,
            "past_interactions": 2
        }
    )

    print("\n=== AGENT FINAL OUTPUT ===")
    print(result)
