import os
import json
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Constants
PROCESSED_CHUNKS_FOLDER = "processed"
CHROMA_DB_FOLDER = "chroma_db"

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_FOLDER)

# Create/Open collection
collection = chroma_client.get_or_create_collection(name="movie_scripts")

def generate_embedding(text):
    """Generates an embedding using Google's text-embedding-gecko."""
    response = genai.embed_content(
        model="models/embedding-001",  # Google's embedding model
        content=text,
        task_type="retrieval_document"
    )
    return response["embedding"]

def process_chunked_scripts():
    """Reads chunked JSON files, generates embeddings, and stores them in ChromaDB."""
    for filename in os.listdir(PROCESSED_CHUNKS_FOLDER):
        if filename.endswith(".json"):
            file_path = os.path.join(PROCESSED_CHUNKS_FOLDER, filename)
            
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            movie_title = data["title"]
            chunks = data["chunks"]

            for chunk in chunks:
                chunk_id = chunk["chunk_id"]
                text = chunk["text"]

                # Generate embedding
                embedding = generate_embedding(text)

                # Store in ChromaDB
                collection.add(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    metadatas=[{"title": movie_title, "chunk_id": chunk_id}],
                    documents=[text]
                )

            print(f"Processed and stored embeddings for: {movie_title}")

if __name__ == "__main__":
    process_chunked_scripts()
