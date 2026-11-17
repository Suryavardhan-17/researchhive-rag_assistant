"""Local, explainable retrieval baseline. No external API key needed."""
from dataclasses import dataclass
from pathlib import Path
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Chunk:
    source: str
    page: int
    text: str

def split_text(text: str, source: str, page: int, size: int = 900, overlap: int = 150) -> list[Chunk]:
    if not (0 <= overlap < size):
        raise ValueError('overlap must be smaller than size')
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return []
    chunks = []
    step = size - overlap
    for start in range(0, len(text), step):
        section = text[start:start + size]
        if section:
            chunks.append(Chunk(source, page, section))
        if start + size >= len(text):
            break
    return chunks

class Retriever:
    def __init__(self):
        self.chunks: list[Chunk] = []
        self.vectorizer = None
        self.matrix = None

    def add(self, chunks: list[Chunk]) -> None:
        self.chunks.extend(chunks)
        if self.chunks:
            self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            self.matrix = self.vectorizer.fit_transform([c.text for c in self.chunks])

    def search(self, question: str, k: int = 3) -> list[dict]:
        if not self.chunks or not question.strip():
            return []
        query = self.vectorizer.transform([question])
        scores = cosine_similarity(query, self.matrix)[0]
        indices = scores.argsort()[::-1][:k]
        return [{'source': self.chunks[i].source, 'page': self.chunks[i].page,
                 'text': self.chunks[i].text, 'score': round(float(scores[i]), 4)}
                for i in indices if scores[i] > 0]

def extract_pdf(fileobj, filename: str) -> list[Chunk]:
    from pypdf import PdfReader
    reader = PdfReader(fileobj)
    if len(reader.pages) > 100:
        raise ValueError('PDF exceeds 100-page demo limit')
    chunks = []
    for index, page in enumerate(reader.pages, 1):
        chunks.extend(split_text(page.extract_text() or '', filename, index))
    return chunks

def evidence_answer(question: str, results: list[dict]) -> str:
    if not results:
        return 'I could not find supporting evidence in the uploaded documents.'
    return ('Relevant passages for: ' + question + '\n\n' +
            '\n\n'.join(f"[{r['source']}, page {r['page']}] {r['text'][:450]}" for r in results))
