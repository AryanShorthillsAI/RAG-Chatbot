# Christopher Nolan Movie Scripts - Retrieval-Augmented Generation (RAG) System  

## 1. Introduction  

### 1.1 Project Overview  
This project is a **Retrieval-Augmented Generation (RAG) system** designed to query Christopher Nolan’s movie scripts. It scrapes, processes, embeds, and stores scripts in **ChromaDB**, then retrieves relevant passages to answer user queries using **Gemini 1.5 Pro**.  

### 1.2 Objectives  
- Scrape and download Christopher Nolan's movie scripts.  
- Extract and process script text from PDF format.  
- Chunk the text for optimal storage and better retrieval.  
- Generate embeddings and store them in ChromaDB.  
- Implement a query system using Gemini 1.5 Pro.  
- Evaluate the system using a golden dataset and RAGAS evaluation.  
- Provide a frontend for user interaction and log user queries.  

---

## 2. System Architecture  

### 2.1 Project Structure
![Architecture image]([/data_sample/Project_structue.png](https://github.com/AryanShorthillsAI/RAG-Chatbot/blob/main/data_sample/Project_structure.png))

### 2.2 High-Level Design  
The system consists of three main components:  

#### **Data Processing**  
- **Web Scraper** (`scraper.py`) - Scrapes and downloads scripts.  
- **Text Extractor** (`extractor.py`) - Extracts text from PDF scripts.  
- **Text Chunker** (`chunker.py`) - Splits extracted text into smaller chunks.  

#### **Embedding & Retrieval**  
- **Embedding Generator** (`embedder.py`) - Generates embeddings using **Gemini text-embedding-004**.  
- **Vector Database** - Stores embeddings using **ChromaDB**.  

#### **Query & Response System**  
- **Query Processor** (`query.py`) - Retrieves script chunks and generates answers using **Gemini 1.5 Pro**.  
- **API Backend** (`backend/main.py`) - Provides a FastAPI backend for querying.  
- **Frontend Interface** (`frontend/app.py`) - Streamlit-based UI for querying and viewing logs.  

### 2.3 Technology Stack  

| Component            | Technology               |  
|----------------------|-------------------------|  
| **Web Scraping**    | BeautifulSoup, Requests  |  
| **Text Extraction** | PyMuPDF (fitz)           |  
| **Text Chunking**   | `tiktoken`               |  
| **Embedding Model** | Gemini text-embedding-004 |  
| **Vector Database** | ChromaDB                 |  
| **Query Processing** | Gemini 1.5 Pro          |  
| **API Backend**    | FastAPI                   |  
| **Frontend**        | Streamlit                |  

---

## 3. Data Processing  

### 3.1 Web Scraping (`scraper.py`)  
- Scrapes scripts from an online source.  
- Extracts script page URLs and identifies download links.  
- Downloads PDFs while skipping Google Drive links.  
- Saves scripts in the `scripts/` directory.  

**Example Output:**  
``` 
Downloading script: Inception (2010)
Saving to: scripts/Inception_2010.pdf
```

### 3.2 Text Extraction (`extractor.py`)  
- Converts PDFs to text.  
- Cleans and normalizes the extracted text.  
- Saves processed text in JSON format in `processed/`.  

**Example JSON Output:**  
```json
{
  "title": "Inception (2010)",
  "text": "COBB: What is the most resilient parasite? An idea..."
}
```

### 3.3 Text Chunking (chunker.py)
- Splits extracted text into fixed-size chunks (512 tokens, 50% overlap).
- Assigns chunk_id based on the movie title.
- Saves chunked text in `processed_chunks/`.

**Example JSON Output:**

```json
{
  "chunk_id": "inception_001",
  "text": "COBB: What is the most resilient parasite?..."
}
```

## 4. Embedding & Retrieval

### 4.1 Embedding Generation (embedder.py)
- Converts text chunks into vector embeddings using Gemini text-embedding-004.
- Stores embeddings in ChromaDB for retrieval.


### 4.2 ChromaDB Storage
- Converts text chunks into vector embeddings using Gemini text-embedding-004.
- Stores embeddings in ChromaDB for retrieval.

| Field            | Type               |  Description |
|----------------------|-------------------------|---------------|  
| **chunk_id**    | string  | Unique identifier for each chunk | 
| **Text** | string           |  Text content of the chunk |

---

## 5 Query Processing 

### 5.1 Query handling (query.py)
- Converts the user query into an embedding.
- Retrieves most relevant script chunks from ChromaDB.
- Passes retrieved chunks to Gemini 1.5 Pro for answer generation.
- Returns the final answer.

**Example input**

```json
{ "query": "Who is Cobb in Inception?" }
```

**Example output**

```json
{ "answer": "Cobb is the main protagonist in Inception." }
```

## 6 API Backend (backend/main.py)

### 6.1 FastAPI Endpoints

| Method           | endpoint               |  Description |
|----------------------|-------------------------|---------------|  
| **/post**    | /query  | Accepts user query and returns an answer | 

---


## 7. Frontend (frontend/app.py)

### 7.1 User Interface
- Accepts user queries.
- Sends the query to the FastAPI backend.
- Displays the retrieved answer.

### 7.2 Example UI flow:

- User types: `"Who is the main character in Memento?"`
- Frontend sends request to backend.
- Backend retrieves relevant chunks and generates a response.
- UI displays: `"Leonard Shelby is the protagonist in Memento."`

## 8 Logging System

### 8.1 Query Logging (logger.py)
- Maintains a log of all user queries and responses.

**Example query**
``` json
{
  "timestamp": "2025-03-16 15:30:45",
  "query": "Who is Cobb?",
  "response": "Cobb is the protagonist in Inception."
}
```

## 9. Evaluation (evaluate_ragas.py)

### 9.1 Performance Measurement
- Uses RAGAS to evaluate the system's accuracy.
- Compares responses to ground-truth answers from a golden dataset.

## 10. Running the System

**Step 1: Install dependencies**

```pip install -r requirements.txt```

**Step 2: Start Backend**

```uvicorn backend.main:app --reload```


**Step 3: Start Frontend**

```streamlit run frontend/app.py```
