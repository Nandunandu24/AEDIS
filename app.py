import streamlit as st
from datetime import datetime

# Core agent
from agent.agent_loop import run_agent

# Analysis utilities
from agent.sentiment import analyze_sentiment
from agent.sla_utils import sla_status
from agent.cost_engine import cost_breakdown
from agent.metrics import sla_metrics
from agent.memory import load_events

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Decision Intelligence Agent",
    layout="wide"
)

st.title("📧 Autonomous Decision Intelligence Agent")
st.caption("Cost-aware • SLA-aware • Explainable • Human-in-the-loop")

# ===============================
# SECTION 1: SINGLE EMAIL
# ===============================
st.subheader("✉️ Single Email Processing")

email_text = st.text_area(
    "Paste customer email",
    height=180,
    placeholder="Example: I requested a refund 3 days ago and want to check the status..."
)

created_at_date = st.date_input(
    "Email received date",
    value=datetime.utcnow().date()
)

run_single = st.button("▶ Run Agent on Single Email")

if run_single and email_text.strip():

    sentiment = analyze_sentiment(email_text)

    meta = {
        "sentiment": sentiment,
        "created_at": datetime.combine(
            created_at_date, datetime.min.time()
        ).isoformat()
    }

    result = run_agent(email_text, meta)

    decision = result["decision"]["final_decision"]
    confidence = result["decision"]["ml_output"]["confidence"]
    route = result.get("route", "N/A")

    # -------- Decision Summary --------
    st.subheader("🧠 Agent Decision Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Final Decision", decision.upper())
    c2.metric("Route", route)
    c3.metric("Confidence", f"{confidence:.2f}")
    c4.metric("Sentiment", sentiment)

    # -------- SLA Visualization --------
    st.subheader("⏱ SLA Status")

    sla = sla_status(decision, meta["created_at"])

    if sla:
        if sla.get("breached"):
            st.error("❌ SLA BREACHED — forced escalation")
        else:
            st.success("✅ SLA ACTIVE")

        st.progress(sla.get("progress", 0.0))

        remaining_minutes = sla.get("remaining_minutes", 0)
        remaining_hours = round(remaining_minutes / 60, 2)
        st.metric("⏳ SLA Remaining (hours)", remaining_hours)
    else:
        st.info("No SLA defined for this decision type.")

    # -------- Cost Breakdown --------
    st.subheader("💰 Cost-Based Decision Breakdown")
    st.bar_chart(cost_breakdown(confidence))

    # -------- Auto Response --------
    st.subheader("📨 Auto-Generated Customer Response")
    if result.get("customer_response"):
        st.success(result["customer_response"])
    else:
        st.warning("No auto-response generated (human review / escalation).")

    # -------- Explanation --------
    st.subheader("📊 Decision Explanation")
    st.markdown(
        f"""
        🧠 **Why the agent made this decision**

        {result["explanation"]}
        """
    )

# ===============================
# SECTION 2: BATCH EMAIL PROCESSING
# ===============================
st.subheader("📂 Batch Email Processing")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    from agent.batch_processor import process_email_batch

    batch_results = process_email_batch(uploaded_file)

    st.success("Batch processed successfully")
    st.dataframe(batch_results)

    st.download_button(
        "⬇ Download Results",
        batch_results.to_csv(index=False),
        "processed_emails.csv",
        "text/csv"
    )

# ===============================
# SECTION 3: HISTORICAL METRICS
# ===============================
st.subheader("📈 Historical SLA Metrics")

events = load_events(limit=200)
metrics = sla_metrics(events)

m1, m2 = st.columns(2)
m1.metric("Total Processed Cases", metrics["total_cases"])
m2.metric("SLA Breach Rate", metrics["sla_breach_rate"])
