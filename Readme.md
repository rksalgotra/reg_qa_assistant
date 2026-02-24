# 🏦 Regulatory Policy Q&A Assistant — POC

A Retrieval-Augmented Generation (RAG) assistant for internal bank policy Q&A.
Built for GitHub Copilot API Gateway (GPT-4o, Gemini 2.5 Pro, etc.)

---

## Architecture

```
Synthetic Policy Docs
      ↓
Chunk + Embed  ←── sentence-transformers (runs locally, ~80MB model)
      ↓
FAISS Vector Index  ←── in-memory, no external DB
      ↓
User Query → Top-K Retrieval → Prompt Construction
      ↓
GitHub Copilot API Gateway (GPT-4o / Gemini 2.5 Pro / o3-mini)
      ↓
Streamlit UI — Answer + Source Chunks
```

**Data privacy**: Only retrieved policy text + the user's question leave the machine.
Embeddings and retrieval are fully local.

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your GitHub Token
```bash
export GITHUB_TOKEN="your_github_pat_here"
```
Or paste it into the sidebar when the app runs.

### 3. Run
```bash
streamlit run app.py
```

---

## Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `rag_engine.py` | Chunking, embedding, FAISS index, retrieval |
| `synthetic_policies.py` | Dummy policy documents (replace with real ones) |
| `requirements.txt` | Python dependencies |

---

## Replacing Synthetic Data with Real Docs

To plug in real policy PDFs:

```python
# Add to requirements.txt:
# pypdf>=3.0.0

from pypdf import PdfReader

def load_pdf(path: str, doc_id: str, title: str) -> dict:
    reader = PdfReader(path)
    text   = "\n".join(page.extract_text() for page in reader.pages)
    return {"id": doc_id, "title": title, "content": text}

# Then pass to engine.build_index([...])
```

---

## Extending the POC

| Feature | How |
|---------|-----|
| **Multi-model comparison** | Call two models with same prompt, display side-by-side |
| **Confidence scoring** | Use retrieval scores to warn when answer confidence is low |
| **Conversation memory** | Pass prior Q&A pairs into the LLM messages array |
| **Feedback logging** | Add 👍/👎 buttons, log to CSV for eval dataset creation |
| **Switch to real docs** | Replace `synthetic_policies.py` with PDF loader |

---

## Sample Questions to Try

- "What CIBIL score is required for a home loan?"
- "When must an STR be filed with FIU-IND?"
- "What documents does a corporate customer need for KYC?"
- "Can customer data be used for AI training?"
- "Who approves loans above INR 1 crore?"
- "What is the bank's zero liability policy for fraud?"
