# ResearchHive — AI-Powered Document Q&A

**A local Retrieval-Augmented Generation (RAG) application powered by Llama 3.2, FastAPI, Streamlit, and Ollama.**

ResearchHive transforms text-based PDF documents into an interactive question-answering experience. Instead of manually searching through lengthy documents, users can ask questions in natural language and receive AI-generated answers alongside supporting document passages and page references.

The application combines traditional information retrieval with a locally running large language model, demonstrating an end-to-end RAG workflow without relying on a paid cloud LLM API.

## Project Overview

Organizations frequently work with lengthy technical documents, research reports, and internal knowledge resources. Finding relevant information manually can be time-consuming.

ResearchHive addresses this problem by providing a simple workflow:

1. Upload a PDF document.
2. Extract and index its text.
3. Ask a question in natural language.
4. Retrieve the most relevant document passages.
5. Generate an answer using Llama 3.2.
6. Display the supporting evidence and page references.

**Project focus:** Document processing, information retrieval, LLM integration, API development, and evidence-grounded question answering.

## Application Demo

### ResearchHive in Action

Add a screenshot of the working application here.

The screenshot should show:
- A question submitted through the Streamlit interface
- An AI-generated answer
- Retrieved evidence with document names and page references

This demonstrates the application's end-to-end functionality.

## Key Features

- **PDF Processing:** Upload text-based PDF files and extract their content.
- **Document Chunking:** Split extracted text into searchable passages.
- **Information Retrieval:** Use TF-IDF vectorization and cosine similarity to identify relevant passages.
- **Local LLM Integration:** Generate answers using Llama 3.2 (3B) through Ollama.
- **Evidence-Based Responses:** Supply retrieved document passages as context for answer generation.
- **Source Transparency:** Display supporting passages with source filenames and page references.
- **REST API:** Expose document upload, question answering, and health-check endpoints through FastAPI.
- **Interactive Interface:** Provide a browser-based application using Streamlit.
- **Local Inference:** Run the language model locally without requiring a paid cloud LLM API.

## System Architecture

```text
                 USER
                   |
                   v
            Streamlit UI
                   |
          +--------+--------+
          |                 |
          v                 v
      Upload PDF        Ask Question
          |                 |
          v                 |
     FastAPI Backend        |
          |                 |
          v                 |
     PDF Text Extraction    |
          |                 |
          v                 |
     Document Chunking      |
          |                 |
          v                 |
       TF-IDF Index         |
          |                 |
          +--------+--------+
                   |
                   v
          Cosine Similarity
                   |
                   v
        Top Relevant Passages
                   |
                   v
            Ollama API
                   |
                   v
             Llama 3.2
                   |
                   v
         AI-Generated Answer
                   |
                   v
      Answer + Retrieved Evidence
                   |
                   v
             Streamlit UI
```

### Retrieval-Augmented Generation Workflow

**1. Ingestion**

The backend extracts text from uploaded PDFs and divides it into smaller passages while retaining source and page information.

**2. Retrieval**

The application uses TF-IDF representations and cosine similarity to rank document passages against the user's question.

**3. Context Construction**

The highest-ranked passages are assembled into a context containing document source names, page numbers, and extracted text.

**4. Generation**

The context and user question are passed to Llama 3.2 through Ollama. The model is instructed to generate an answer using the retrieved information.

**5. Evidence Display**

The Streamlit interface displays the generated answer and the retrieved supporting passages, allowing users to inspect the underlying evidence.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Frontend | Streamlit |
| Language Model | Llama 3.2 (3B) |
| Local LLM Runtime | Ollama |
| Information Retrieval | TF-IDF |
| Similarity Ranking | Cosine Similarity |
| PDF Extraction | pypdf |
| API Communication | HTTP / REST |
| Testing | pytest |
| Version Control | Git and GitHub |

## Getting Started

### Prerequisites

- Python 3.11 or later
- Git
- Ollama
- Sufficient memory and disk space to run Llama 3.2 locally

### 1. Clone the Repository

```bash
git clone https://github.com/SuryaVardhan-17/researchhive-rag_assistant.git
cd researchhive-rag_assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
python -m pip install ollama
```

### 4. Install and Configure Ollama

Download Ollama from:

https://ollama.com

Pull the language model:

```bash
ollama pull llama3.2:3b
```

Ensure the Ollama service is running before submitting questions.

### 5. Start the FastAPI Backend

In the first terminal:

```bash
python -m uvicorn app.api:app --reload --port 8000
```

The backend runs at:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs

### 6. Start the Streamlit Frontend

Open a second terminal and activate the virtual environment.

```bash
streamlit run ui.py
```

Open the application:

http://localhost:8501

### 7. Use ResearchHive

1. Select a text-based PDF.
2. Click **Index PDF**.
3. Enter a question about the document.
4. Click **Search**.
5. Review the AI-generated answer and supporting evidence.

The first request may take longer while the local model initializes.

## Example Use Case

**Document:** A technical PDF discussing enterprise identity and access management.

**User question:**

What is the difference between authentication and authorization?

**Example answer:**

Authentication verifies who a user is, while authorization determines which resources that user is permitted to access.

**Supporting evidence:**

The application displays relevant excerpts from the uploaded PDF, including their source filename and page number.

This allows users to compare the model's answer with the retrieved document content.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check backend health and indexed chunk count |
| POST | `/documents` | Upload and index a PDF |
| POST | `/ask` | Retrieve evidence and generate an answer |

The `/ask` endpoint accepts a question and an optional retrieval limit (`top_k`).

Responses include the generated answer, retrieved citations, and generation metadata.

## Testing

Run the automated tests from the repository root:

```bash
python -m pytest -q
```

The existing tests provide baseline checks for the project's core functionality. Additional tests for LLM answer quality, citation faithfulness, and full API integration are future improvements.

### Manual Validation

The application has also been tested through its browser interface by:

- Uploading and indexing a PDF
- Retrieving relevant document passages
- Generating a local Llama 3.2 answer
- Displaying source passages and page references

## Design Decisions

### Why TF-IDF?

TF-IDF provides a lightweight, interpretable retrieval baseline without requiring a separate embedding model or vector database.

It is useful for demonstrating document indexing, passage ranking, and retrieval integration before introducing more advanced semantic search.

### Why Ollama?

Ollama allows language models to run locally, reducing dependency on external inference APIs and making the application suitable for local experimentation.

### Why FastAPI and Streamlit?

FastAPI separates backend document processing and model orchestration from the user interface.

Streamlit provides a lightweight interface for demonstrating the complete application workflow.

## Current Limitations

- Only text-based PDFs are supported; scanned PDFs require OCR.
- Retrieval relies on lexical TF-IDF matching rather than semantic embeddings.
- The document index is maintained in memory and is not designed as a persistent, multi-user document store.
- Model responses may contain inaccuracies or unsupported claims.
- Displayed citations represent retrieved supporting passages; individual generated claims are not automatically verified.
- Local inference performance depends on available hardware.
- The application is a local demonstration, not a production-hardened service.

## Future Enhancements

- Semantic retrieval using dense embeddings
- FAISS or another vector database
- Hybrid search combining lexical and semantic retrieval
- Reranking for improved passage relevance
- Persistent document indexing
- Retrieval and generation evaluation
- Citation faithfulness checks
- Improved error handling and performance monitoring
- Containerization and deployment

## What This Project Demonstrates

ResearchHive provides hands-on experience across several AI engineering components:

- Building an end-to-end RAG pipeline
- Designing document ingestion and retrieval workflows
- Integrating locally hosted language models
- Developing REST APIs with FastAPI
- Building interactive interfaces with Streamlit
- Structuring evidence-grounded LLM responses
- Testing and debugging a multi-component Python application
