# Autonomous Decision Intelligence Email System (AEDIS)

## Overview
AEDIS is an enterprise-style autonomous decision intelligence system designed to process customer emails, make policy-aware decisions, enforce SLAs, optimize cost, and generate safe automated responses with human-in-the-loop escalation.

## Key Features
- Policy-based decision making
- SLA-aware escalation logic
- Cost-based action optimization
- Auto-response generation with safety guardrails
- Batch email processing
- Explainability for every decision
- Streamlit operations dashboard

## Architecture
Email → Reasoning (Policy + Cost + SLA) → Routing → Execution → Explanation → Storage

## Tech Stack
- Python
- Streamlit
- Scikit-learn
- FastAPI (for future integrations)
- Rule-based + ML-assisted reasoning

## How to Run Locally

https://jrg5dffummgve25heuoa66.streamlit.app/
```bash

pip install -r requirements.txt
streamlit run app.py

