from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from bot import FAQBot  # Make sure this has a .ask(question) method

app = FastAPI(title="FAQ Bot API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the FAQBot
bot = FAQBot(
    faq_path="faq.txt",                      # Path to your FAQ file
    escalation_url="http://127.0.0.1:8001/escalate"  # Dummy escalation endpoint
)

# Request model
class AskRequest(BaseModel):
    question: str

# API endpoint
@app.post("/ask")
async def ask_bot(req: AskRequest):
    try:
        # Ensure question is provided and not empty
        if not req.question or not req.question.strip():
            return {
                "answer_text": "Please provide a valid question.",
                "confidence": {"score": 0.0, "label": "low"},
                "source_reference": "",
                "escalated_to_human": False,
                "escalation_request_id": None
            }
        
        # Pass the question to the bot
        question = req.question.strip()
        response = bot.ask(question)
        
        # Ensure response always has answer_text
        return {
            "answer_text": response.get("answer_text", "No answer available."),
            "confidence": response.get("confidence", {}),
            "source_reference": response.get("source_reference", ""),
            "escalated_to_human": response.get("escalated_to_human", False),
            "escalation_request_id": response.get("escalation_request_id", None)
        }
    except Exception as e:
        return {
            "answer_text": f"Sorry, something went wrong: {str(e)}",
            "confidence": {},
            "source_reference": "",
            "escalated_to_human": False,
            "escalation_request_id": None
        }
