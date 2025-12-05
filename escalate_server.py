from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI(title="Escalation Server")

class EscalationRequest(BaseModel):
    question: str
    snippet: str
    attempted_answer: str
    confidence: float

@app.post("/escalate")
async def escalate(req: EscalationRequest):
    request_id = str(uuid.uuid4())
    return {
        "status": "received",
        "request_id": request_id,
        "human_team_message": "Your issue has been forwarded."
    }
