from fastapi import FastAPI
from api.schemas import AgentRequest, AgentResponse
from agent.agent_loop import run_agent

app = FastAPI(
    title="Agentic Decision Intelligence API",
    description="Autonomous agent that reasons, plans, acts, and self-corrects",
    version="1.0.0"
)


@app.post("/agent/run", response_model=AgentResponse)
def run_agent_endpoint(request: AgentRequest):
    """
    Run the full agent loop.
    """
    result = run_agent(
        email_text=request.email_text,
        meta=request.meta
    )
    return result
