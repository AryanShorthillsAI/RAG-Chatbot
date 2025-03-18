from fastapi import FastAPI, Request
import json
import datetime
from query import generate_answer  # Import from query.py

app = FastAPI()

LOG_FILE = "logs/query_logs.json"

# Function to log interactions
def log_interaction(query, response):
    log_entry = {
        "timestamp": str(datetime.datetime.now()),
        "query": query,
        "response": response
    }
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4)

@app.post("/query")
async def process_query(request: Request):
    data = await request.json()
    query = data.get("query", "")

    if not query:
        return {"error": "No query provided"}

    # Generate response using RAG
    response = generate_answer(query)

    # Log the query and response
    log_interaction(query, response)

    return {"query": query, "response": response}
