"""
RAG Engine - handles document chunking, embedding and retrieval.
Runs entirely locally (no data sent externally during indexing).
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple


EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # small, fast, good quality — downloads once, runs locally
CHUNK_SIZE      = 400   # characters per chunk (tweak based on your doc structure)
CHUNK_OVERLAP   = 80    # overlap to avoid cutting context at chunk boundaries


def chunk_document(doc: Dict, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[Dict]:
    """Split a document into overlapping text chunks."""
    text    = doc["content"].strip()
    chunks  = []
    start   = 0

    while start < len(text):
        end   = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "doc_id"   : doc["id"],
                "doc_title": doc["title"],
                "chunk_id" : f"{doc['id']}_chunk_{len(chunks)}",
                "text"     : chunk,
            })

        start += chunk_size - overlap

    return chunks


class RAGEngine:
    def __init__(self):
        self.embedder  = None
        self.index     = None
        self.chunks    : List[Dict] = []
        self.dimension : int        = 0

    def build_index(self, documents: List[Dict]) -> int:
        """Chunk all documents, embed them, and build a FAISS index. Returns chunk count."""
        print("Loading embedding model (first run downloads ~80MB)...")
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)

        # Chunk all docs
        all_chunks = []
        for doc in documents:
            all_chunks.extend(chunk_document(doc))
        self.chunks = all_chunks

        # Embed
        print(f"Embedding {len(all_chunks)} chunks...")
        texts      = [c["text"] for c in all_chunks]
        embeddings = self.embedder.encode(texts, show_progress_bar=False)
        embeddings = np.array(embeddings, dtype="float32")

        # Normalise for cosine similarity via inner product
        faiss.normalize_L2(embeddings)

        # Build FAISS flat index (exact search — fast enough for small corpora)
        self.dimension = embeddings.shape[1]
        self.index     = faiss.IndexFlatIP(self.dimension)
        self.index.add(embeddings)

        print(f"Index built: {self.index.ntotal} chunks across {len(documents)} documents.")
        return len(all_chunks)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Embed a query and retrieve the top_k most relevant chunks."""
        if self.index is None or self.embedder is None:
            raise RuntimeError("Index not built. Call build_index() first.")

        query_vec = self.embedder.encode([query], show_progress_bar=False)
        query_vec = np.array(query_vec, dtype="float32")
        faiss.normalize_L2(query_vec)

        scores, indices = self.index.search(query_vec, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            chunk = self.chunks[idx].copy()
            chunk["score"] = float(score)
            results.append(chunk)

        return results


def build_prompt(query: str, retrieved_chunks: List[Dict]) -> str:
    """Construct the RAG prompt — keeps system instructions clean and cited."""
    context_blocks = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        context_blocks.append(
            f"[Source {i} — {chunk['doc_title']} ({chunk['doc_id']})]:\n{chunk['text']}"
        )
    context = "\n\n".join(context_blocks)

    prompt = f"""You are a knowledgeable regulatory compliance assistant for a bank.
Answer the question below using ONLY the policy excerpts provided.
If the answer is not found in the excerpts, say "This information is not covered in the available policy documents."
Always cite the Source number (e.g. [Source 1]) when referencing policy content.
Be precise, professional, and concise.

--- POLICY EXCERPTS ---
{context}
-----------------------

Question: {query}

Answer:"""
    return prompt
