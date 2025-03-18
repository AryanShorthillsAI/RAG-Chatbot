import chromadb

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_collection(name="movie_scripts")

# Get all stored documents
# print(collection.peek())  # Shows a sample of stored embeddings
# print(collection.count())  # Returns number of stored embeddings
results = collection.get(
    where={"title": "INCEPTION"},  # Change title as needed
    include=["embeddings", "documents", "metadatas"]
)

print(results)
