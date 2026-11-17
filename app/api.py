from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from io import BytesIO
from .core import Retriever, extract_pdf, evidence_answer

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
    results = retriever.search(payload.question, payload.top_k)
    return {'answer': evidence_answer(payload.question, results), 'citations': results,
            'generation_mode': 'extractive (no LLM)'}
