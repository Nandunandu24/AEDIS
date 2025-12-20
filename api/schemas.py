from pydantic import BaseModel
from typing import Dict, Any


class AgentRequest(BaseModel):
    email_text: str
    meta: Dict[str, Any]


class AgentResponse(BaseModel):
    decision: Dict[str, Any]
    action_plan: Dict[str, Any]
    execution_result: Dict[str, Any]
    feedback: Dict[str, Any]
