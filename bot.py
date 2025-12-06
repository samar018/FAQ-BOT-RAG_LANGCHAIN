import requests
from retriever import FAQRetriever

THRESHOLD = 0.30  # confidence threshold

class FAQBot:
    def __init__(self, faq_path, escalation_url):
        self.retriever = FAQRetriever(faq_path)
        self.escalation_url = escalation_url

    def classify_confidence(self, score):
        if score >= 0.50:
            return "high"
        elif score >= 0.30:
            return "medium"
        else:
            return "low"

    def ask(self, query):
        # Ensure query is not empty
        if not query or not query.strip():
            return {
                "answer_text": "Please provide a valid question.",
                "confidence": {"score": 0.0, "label": "low"},
                "source_reference": "",
                "escalated_to_human": False,
                "escalation_request_id": None
            }
        
        # Search with the query
        results = self.retriever.search(query.strip())
        
        # Check if results are empty
        if not results or len(results) == 0:
            return {
                "answer_text": "No matching FAQ found.",
                "confidence": {"score": 0.0, "label": "low"},
                "source_reference": "",
                "escalated_to_human": False,
                "escalation_request_id": None
            }
        
        best_line, best_score = results[0]

        label = self.classify_confidence(best_score)
        answer = f"Based on the FAQ: {best_line}" if best_score > 0 else "FAQ does not contain information."

        response = {
            "answer_text": answer,
            "confidence": {"score": float(best_score), "label": label},
            "source_reference": best_line,
            "escalated_to_human": False,
            "escalation_request_id": None
        }

        if best_score < THRESHOLD:
            payload = {
                "question": query,
                "snippet": best_line,
                "attempted_answer": answer,
                "confidence": best_score
            }
            try:
                r = requests.post(self.escalation_url, json=payload)
                response["escalated_to_human"] = True
                response["escalation_request_id"] = r.json().get("request_id")
            except Exception:
                response["escalated_to_human"] = True
                response["escalation_request_id"] = "error_sending_escalation"

        return response

if __name__ == "__main__":
    bot = FAQBot(
        faq_path="faq.txt",
        escalation_url="http://127.0.0.1:8000/escalate"
    )

    while True:
        q = input("You: ")
        res = bot.ask(q)
        print(res)
