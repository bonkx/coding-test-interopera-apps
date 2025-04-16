import json
import re

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# setup allowed origins for CORS
origins = [
    "http://localhost:3000",
]

# setup CORS middleware
# This allows the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_dummy_data():
    # Load dummy data from a JSON file
    with open("dummyData.json", "r") as f:
        return json.load(f)


@app.get("/api/sales-reps")
def get_data_sales_reps():
    """
    Returns dummy data (e.g., list of sales-reps).
    """
    try:
        data = load_dummy_data()
        return data
        # raise ValueError("Failed to fetch data")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/chart/deal-value-per-rep")
def deal_value_per_rep():
    try:
        data = load_dummy_data()
        SALES_REPS = data["salesReps"]

        labels = []
        values = []
        for rep in SALES_REPS:
            labels.append(rep["name"])
            total = sum(deal["value"] for deal in rep["deals"])
            values.append(total)

        return {
            "labels": labels,
            "datasets": [{
                "label": "Total Deal Value",
                "data": values,
                "backgroundColor": "#36A2EB"
            }]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/chart/top-clients")
def top_clients():
    try:
        data = load_dummy_data()
        SALES_REPS = data["salesReps"]

        clients = []
        for rep in SALES_REPS:
            for deal in rep["deals"]:
                if deal["status"] == "Closed Won":
                    clients.append({"client": deal["client"], "value": deal["value"]})

        # Sort by value descending
        clients = sorted(clients, key=lambda x: x["value"], reverse=True)[:5]

        return {
            "labels": [c["client"] for c in clients],
            "datasets": [{
                "label": "Top Clients by Deal Value",
                "data": [c["value"] for c in clients],
                "backgroundColor": "#FFC107"
            }]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


class AIRequest(BaseModel):
    question: str


def clean_input(text: str) -> str:
    return re.sub(r'[^\w\s]', '', text.lower()).strip()


def classify_intent(text: str) -> str:
    greetings = ["hi", "hello", "hey"]
    farewell = ["bye", "goodbye", "see you"]
    help_requests = ["help", "support", "need assistance", "can you help"]
    feelings = ["how are you", "how is it going", "are you ok"]
    thanks = ["thank you", "thanks", "appreciate it"]

    if any(kw in text for kw in greetings):
        return "greeting"
    elif any(kw in text for kw in farewell):
        return "farewell"
    elif any(kw in text for kw in help_requests):
        return "help"
    elif any(kw in text for kw in feelings):
        return "feeling"
    elif any(kw in text for kw in thanks):
        return "thanks"
    else:
        return "unknown"


# Mock function to simulate AI response
def generate_response(intent: str, text: str) -> str:
    if intent == "greeting":
        return "Hi there! 👋 How can I assist you today?"
    elif intent == "farewell":
        return "Goodbye! Hope to talk again soon!"
    elif intent == "help":
        return "Sure, I can help! Tell me what you need assistance with."
    elif intent == "feeling":
        return "I'm just a bunch of code, but I'm doing great! 😄 How about you?"
    elif intent == "thanks":
        return "You're welcome! Let me know if there's anything else I can help with."
    else:
        # Slightly smarter fallback
        if "weather" in text:
            return "I can't provide real weather data, but it looks sunny in your heart! ☀️"
        elif "joke" in text:
            return "Why don't programmers like nature? Too many bugs. 😂"
        elif "time" in text:
            from datetime import datetime
            return f"It's currently {datetime.now().strftime('%H:%M:%S')}."
        else:
            return "I'm not sure how to respond to that yet. Can you rephrase?"


@app.post("/api/ai")
async def ai_endpoint(request: AIRequest):
    """
    Accepts a user question and returns a placeholder AI response.
    (Optionally integrate a real AI model or external service here.)
    """
    user_question = clean_input(request.question)

    # Placeholder logic: echo the question or generate a simple response
    # Replace with real AI logic as desired (e.g., call to an LLM).
    # return {"answer": f"This is a placeholder answer to your question: {user_question}"}
    try:
        intent = classify_intent(user_question)
        answer = generate_response(intent, user_question)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
