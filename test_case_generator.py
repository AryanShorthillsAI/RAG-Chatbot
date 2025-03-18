import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load extracted entities
with open("test_data/entities.json", "r", encoding="utf-8") as file:
    entities = json.load(file)

def generate_question(entity):
    """Generates a trivia question about the given entity using Gemini."""
    prompt = f"Generate a trivia question about '{entity}' from Christopher Nolan's movies."

    model = genai.GenerativeModel("models/gemini-1.5-pro")
    response = model.generate_content(prompt)

    return response.text.strip() if response and response.text else "No question generated."

# Generate 1000 test questions
test_questions = [{"question": generate_question(entity)} for entity in entities[:1000]]

# Save questions to JSON
os.makedirs("test_data", exist_ok=True)
with open("test_data/test_questions.json", "w", encoding="utf-8") as file:
    json.dump(test_questions, file, indent=4)

print("\n✅ **100 Test Questions Saved in `test_questions.json`**")
