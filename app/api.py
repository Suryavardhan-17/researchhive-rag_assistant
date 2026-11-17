from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from io import BytesIO
from .core import Retriever, extract_pdf, evidence_answer
from ollama import chat

app = FastAPI(title='ResearchHive - Evidence-First Document Q&A')
retriever = Retriever()

class Query(BaseModel):
    question: str = Field(min_length=2, max_length=1000)
    top_k: int = Field(default=3, ge=1, le=10)

@app.get('/health')
def health():
    return {'status': 'ok', 'indexed_chunks': len(retriever.chunks)}

@app.post('/documents')
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(400, 'Upload a PDF file')
    content = await file.read(10 * 1024 * 1024 + 1)
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(413, 'Maximum upload size is 10 MB')
    try:
        chunks = extract_pdf(BytesIO(content), file.filename)
        if not chunks:
            raise HTTPException(422, 'No extractable text found; scanned PDFs need OCR')
        retriever.add(chunks)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(422, 'Could not parse PDF') from exc
    return {'filename': file.filename, 'chunks_added': len(chunks)}

@app.post('/ask')
def ask(payload: Query):
    # Step 1: Find relevant passages from the PDF
    results = retriever.search(payload.question, payload.top_k)

    # Step 2: Handle questions with no matching evidence
    if not results:
        return {
            'answer': 'No relevant evidence found in the uploaded documents.',
            'citations': [],
            'generation_mode': 'no evidence'
        }

    # Step 3: Prepare the retrieved PDF passages
    context = "\n\n".join(
        f"Source: {item['source']}, Page: {item['page']}\n{item['text']}"
        for item in results
    )

    # Step 4: Ask Llama 3.2 to generate an answer
    response = chat(
        model='llama3.2:3b',
        messages=[
            {
                'role': 'system',
                'content': (
                    'Answer questions using only the provided document context. '
                    'If the context does not contain the answer, say you do not know. '
                    'Do not invent facts. Cite the source and page number.'
                )
            },
            {
                'role': 'user',
                'content': f"Context:\n{context}\n\nQuestion: {payload.question}"
            }
        ]
    )

    # Step 5: Return the AI answer and original citations
    return {
        'answer': response.message.content,
        'citations': results,
        'generation_mode': 'ollama llama3.2:3b'
    }
