import pandas as pd
from datetime import datetime
from agent.agent_loop import run_agent
from agent.sentiment import analyze_sentiment

def process_email_batch(csv_path: str):
    df = pd.read_csv(csv_path)

    results = []

    for _, row in df.iterrows():
        email_text = row["body"]
        received_at = row["received_at"]

        # 🔹 Auto sentiment detection
        sentiment = analyze_sentiment(email_text)

        meta = {
            "sentiment": sentiment,
            "created_at": received_at
        }

        result = run_agent(email_text, meta)

        results.append({
            "email_id": row["email_id"],
            "decision": result["decision"]["final_decision"],
            "confidence": result["decision"]["ml_output"]["confidence"],
            "auto_reply": result.get("customer_response"),
            "route": result.get("route"),
            "timestamp": datetime.utcnow().isoformat()
        })

    return pd.DataFrame(results)
