import os
import json
import spacy

# Load spaCy's NLP model for English
nlp = spacy.load("en_core_web_sm")

PROCESSED_CHUNKS_FOLDER = "processed"
OUTPUT_FILE = "test_data/entities.json"

def extract_entities():
    """Extracts meaningful entities (characters, locations, concepts) using NLP."""
    entity_set = set()

    for filename in os.listdir(PROCESSED_CHUNKS_FOLDER):
        if filename.endswith(".json"):
            filepath = os.path.join(PROCESSED_CHUNKS_FOLDER, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

                for chunk in data["chunks"]:
                    text = chunk["text"]
                    
                    # Use spaCy to extract named entities
                    doc = nlp(text)
                    for ent in doc.ents:
                        if ent.label_ in ["PERSON"]:  # Keep only names, places, orgs
                            entity_set.add(ent.text)

    return list(entity_set)

# Extract refined entities and save to JSON
os.makedirs("test_data", exist_ok=True)
entities = extract_entities()

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(entities, file, indent=4)

print("\n✅ **Refined Entities Saved in `entities.json`**")
