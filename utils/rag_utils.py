import fitz  # PyMuPDF for PDF processing
import os
import json
from sentence_transformers import SentenceTransformer, util

MODEL = SentenceTransformer('all-MiniLM-L6-v2')
KNOWLEDGE_BASE_PATH = "knowledge_base.json"

def process_pdf_upload(uploaded_pdf):
    """Extract text from uploaded PDF and save embeddings."""
    text = ""
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    for page in doc:
        text += page.get_text("text")

    # Save into knowledge base
    kb = load_knowledge_base()
    embeddings = MODEL.encode(text, convert_to_tensor=True)
    kb.append({"text": text, "embedding": embeddings.tolist()})
    save_knowledge_base(kb)


def retrieve_relevant_context(query, top_k=1):
    """Retrieve the most relevant chunk from knowledge base."""
    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        return "No medical knowledge base available."

    kb = load_knowledge_base()
    if not kb:
        return "Knowledge base empty."

    query_emb = MODEL.encode(query, convert_to_tensor=True)
    scores = [util.cos_sim(query_emb, MODEL.encode(k['text'], convert_to_tensor=True)).item() for k in kb]
    best_index = scores.index(max(scores))
    return kb[best_index]['text']


def load_knowledge_base():
    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        return []
    with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_knowledge_base(data):
    with open(KNOWLEDGE_BASE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f)
