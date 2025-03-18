import json
import os
import tiktoken  # Tokenizer for accurate chunking

# Constants
CHUNK_SIZE = 512
OVERLAP = 256
ENCODING = "cl100k_base"  # OpenAI's tokenizer (same as GPT-3.5 Turbo)
PROCESSED_FOLDER = "extracted"  # Folder containing extracted scripts
CHUNKED_FOLDER = "processed"  # New folder to store chunked JSON

def chunk_text(text, movie_name):
    """Splits text into fixed-size overlapping chunks."""
    encoding = tiktoken.get_encoding(ENCODING)
    tokens = encoding.encode(text)

    chunks = []
    for i in range(0, len(tokens), CHUNK_SIZE - OVERLAP):
        chunk_tokens = tokens[i:i + CHUNK_SIZE]
        chunk_text = encoding.decode(chunk_tokens)
        chunk_id = f"{movie_name}_{len(chunks) + 1}"
        chunks.append({"chunk_id": chunk_id, "text": chunk_text})

    return chunks

def process_movie_script(json_path):
    """Reads extracted text, chunks it, and saves chunked JSON in processed/."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    movie_name = data["title"].replace(" ", "_")  # Normalize title
    text = data["text"]

    # Chunk text
    chunks = chunk_text(text, movie_name)

    # Ensure processed_chunks folder exists
    os.makedirs(CHUNKED_FOLDER, exist_ok=True)

    # Save chunked JSON
    output_path = os.path.join(CHUNKED_FOLDER, f"{movie_name}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"title": data["title"], "chunks": chunks}, f, indent=4, ensure_ascii=False)

    print(f"Chunked text saved: {output_path}")

def process_all_scripts():
    """Processes all extracted scripts in 'extracted/' and saves chunks in 'processed/'."""
    for filename in os.listdir(PROCESSED_FOLDER):
        if filename.endswith(".json"):
            process_movie_script(os.path.join(PROCESSED_FOLDER, filename))

if __name__ == "__main__":
    process_all_scripts()
