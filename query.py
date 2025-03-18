import os
import google.generativeai as genai
import chromadb
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")
genai.configure(api_key=api_key)

# # List available models
# print("Available Models:")
# for model in genai.list_models():
#     print(model)

# Connect to ChromaDB
CHROMA_DB_FOLDER = "chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_FOLDER)
collection = chroma_client.get_collection(name="movie_scripts")

def generate_embedding(text):
    """Generates an embedding for the query using the same model as stored chunks."""
    response = genai.embed_content(
        model="models/embedding-001",  # Google's embedding model
        content=text,
        task_type="retrieval_query"
    )
    return response["embedding"]

def get_relevant_chunks(query, top_k=3):
    """Retrieves the top K most relevant chunks from ChromaDB."""
    query_embedding = generate_embedding(query)  # Generate embedding for the query

    results = collection.query(
        query_embeddings=[query_embedding],  # Use correct embeddings
        n_results=top_k,
        include=["documents", "metadatas"]
    )
    
    retrieved_chunks = results["documents"][0] if results["documents"] else []
    return retrieved_chunks

def generate_answer(query):
    """Uses Gemini to generate an answer based on retrieved script context."""
    retrieved_chunks = get_relevant_chunks(query)

    if not retrieved_chunks:
        return "Sorry, I couldn't find relevant information in the scripts."

    # # Print the retrieved chunks before generating the answer
    # print("\n📜 **Retrieved Chunks:**")
    # for i, chunk in enumerate(retrieved_chunks, start=1):
    #     print(f"\n🔹 **Chunk {i}:**\n{chunk}\n" + "-" * 50)

    # Combine retrieved chunks into context
    context = "\n\n".join(retrieved_chunks)
    
    prompt = f"""
    You are an expert at answering questions based on movie scripts.
    Given the following context from a script, answer the user's question.

    Context:
    {context}

    Question: {query}

    Answer:
    """

    # Use the correct Gemini model
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    response = model.generate_content(prompt)
    
    return response.text.strip()

def main():
    """Takes user input and retrieves answers from Gemini."""
    print("🎬 Ask a question about Christopher Nolan's movie scripts (or type 'exit' to quit).")

    while True:
        query = input("\n🔍 Your Question: ")
        if query.lower() == "exit":
            print("👋 Exiting...")
            break
        
        answer = generate_answer(query)
        print("\n🤖 **Gemini's Answer:**", answer)

if __name__ == "__main__":
    main()
