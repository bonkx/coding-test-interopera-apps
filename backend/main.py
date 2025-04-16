import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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


@app.get("/api/chart/top-clients")
def top_clients():
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


@app.post("/api/ai")
async def ai_endpoint(request: Request):
    """
    Accepts a user question and returns a placeholder AI response.
    (Optionally integrate a real AI model or external service here.)
    """
    body = await request.json()
    user_question = body.get("question", "")

    # Placeholder logic: echo the question or generate a simple response
    # Replace with real AI logic as desired (e.g., call to an LLM).
    return {"answer": f"This is a placeholder answer to your question: {user_question}"}

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
