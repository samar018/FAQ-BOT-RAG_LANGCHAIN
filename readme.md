

```markdown
# FAQ Support Bot (FastAPI Version)

A minimal **FAQ support bot** for a single product that answers user questions based on a provided FAQ file.  
The bot decides confidence for each answer and escalates low-confidence questions to a human team via a FastAPI endpoint.

---

## **Features**

- Search FAQ/documentation for relevant answers
- Confidence scoring (high, medium, low)
- Automatic escalation for low-confidence questions
- CLI chat interface
- FastAPI-based escalation endpoint with auto-generated docs

---

## **Project Structure**

```

FAQ bot/
├─ venv/                  # Python virtual environment
├─ faq.txt                # FAQ / documentation file
├─ retriever.py           # FAQ search / cosine similarity logic
├─ bot.py                 # Main CLI bot logic
├─ escalate_server.py     # FastAPI-based escalation endpoint
├─ requirements.txt       # Dependencies
├─ README.md              # Project instructions

````

---

## **Setup Instructions**

### **1. Create and activate virtual environment**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
# or for CMD: venv\Scripts\activate.bat
````

### **2. Install dependencies**

```powershell
pip install -r requirements.txt
```

---

## **3. Run Escalation Server (FastAPI)**

```powershell
uvicorn escalate_server:app --reload --port 8000
```

* Server will run on: `http://127.0.0.1:8000`
* Auto-generated API docs: `http://127.0.0.1:8000/docs`

---

## **4. Run the CLI Bot**

In a new terminal (venv active):

```powershell
python bot.py
```

* Prompt will appear:

```
You:
```

* Type your question about the product, e.g.:

```
You: How do I reset the device?
```

* Bot will return JSON response:

```json
{
  "answer_text": "...",
  "confidence": {"score": 0.69, "label": "high"},
  "source_reference": "...",
  "escalated_to_human": false,
  "escalation_request_id": null
}
```

* Low-confidence questions automatically POST to FastAPI `/escalate` endpoint.

---

## **5. FAQ File**

* File: `faq.txt`
* Format: Each line contains **question + answer**:

```
How do I reset the device? You can reset it by holding the power button for 10 seconds.
How long does the battery last? The battery lasts up to 8 hours on normal usage.
```

* Add more FAQs as needed.

---

## **6. Escalation Behavior**

* Confidence thresholds:

| Score Range | Label  |
| ----------- | ------ |
| >= 0.5      | high   |
| 0.3 – 0.5   | medium |
| < 0.3       | low    |

* Low-confidence questions automatically send POST to FastAPI `/escalate` with:

```json
{
  "question": "User question",
  "snippet": "Best matching FAQ line",
  "attempted_answer": "Bot's answer",
  "confidence": 0.05
}
```

* Server responds with a `request_id`:

```json
{
  "status": "received",
  "request_id": "uuid",
  "human_team_message": "Your issue has been forwarded."
}
```

---

## **7. GitHub Repository**

* Repository URL: [https://github.com/samar018/FAQ-BOT-RAG_LANGCHAIN](https://github.com/samar018/FAQ-BOT-RAG_LANGCHAIN)

### **Push local project to GitHub**

```powershell
git init
git add .
git commit -m "Initial commit: FAQ bot FastAPI version"
git branch -M main
git remote add origin https://github.com/samar018/FAQ-BOT-RAG_LANGCHAIN.git
git push -u origin main
```

* Make sure the repository is **empty** before first push.
* `.gitignore` will ignore `venv/`, logs, cache, etc.

---

## **8. Notes**

* Built with **Python 3.11**, **FastAPI**, and **requests**.
* CLI interface is simple; can be upgraded to web-based chat later.
* Thresholds and cosine similarity logic are configurable.
* Easily extendable to **RAG / embeddings** in the future.

---

## **9. References / Useful Links**

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [Python Virtual Environments](https://docs.python.org/3/library/venv.html)
* [Requests Library](https://docs.python-requests.org/en/latest/)

```
