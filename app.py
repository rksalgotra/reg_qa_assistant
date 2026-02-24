"""
Regulatory Q&A Assistant — POC
Bank internal policy Q&A using RAG + GitHub Copilot API Gateway (GPT / Gemini)

Run with:  streamlit run app.py
"""

import os
import streamlit as st
from openai import OpenAI

from synthetic_policies import DOCUMENTS
from rag_engine import RAGEngine, build_prompt

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

# GitHub Copilot API Gateway — OpenAI-compatible endpoint
COPILOT_BASE_URL = "https://api.githubcopilot.com"

# Models available via GitHub Copilot (add/remove as your gateway allows)
AVAILABLE_MODELS = {
    "GPT-4o"          : "gpt-4o",
    "GPT-4o Mini"     : "gpt-4o-mini",
    "Gemini 2.5 Pro"  : "gemini-2.5-pro",
    "o3-mini"         : "o3-mini",
}

TOP_K_CHUNKS = 5   # number of policy chunks to retrieve per query

# ─────────────────────────────────────────────
# PAGE SETUP
# ─────────────────────────────────────────────

st.set_page_config(
    page_title = "Regulatory Q&A Assistant",
    page_icon  = "🏦",
    layout     = "wide",
)

st.title("🏦 Regulatory Policy Q&A Assistant")
st.caption("Internal use only · Powered by RAG + GitHub Copilot API · Synthetic data POC")

# ─────────────────────────────────────────────
# SIDEBAR — CONFIG
# ─────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Configuration")

    github_token = st.text_input(
        "GitHub Token",
        type     = "password",
        value    = os.environ.get("GITHUB_TOKEN", ""),
        help     = "Your GitHub PAT with Copilot access. Set GITHUB_TOKEN env var to avoid pasting each time.",
    )

    selected_model_label = st.selectbox(
        "LLM Model",
        options = list(AVAILABLE_MODELS.keys()),
        index   = 0,
        help    = "All models routed via GitHub Copilot API Gateway",
    )
    selected_model = AVAILABLE_MODELS[selected_model_label]

    top_k = st.slider(
        "Chunks to retrieve (top-k)",
        min_value = 1, max_value = 10, value = TOP_K_CHUNKS,
        help = "More chunks = more context but longer prompts",
    )

    temperature = st.slider(
        "Temperature",
        min_value = 0.0, max_value = 1.0, value = 0.2, step = 0.05,
        help = "Lower = more factual and deterministic",
    )

    st.divider()
    st.subheader("📄 Loaded Policy Documents")
    for doc in DOCUMENTS:
        st.markdown(f"- **{doc['id']}**: {doc['title']}")

    st.divider()
    st.info(
        "**Data stays local.**\n\n"
        "Embeddings and retrieval run on your machine. "
        "Only the retrieved policy excerpts + your question are sent to the LLM."
    )

# ─────────────────────────────────────────────
# BUILD RAG INDEX (cached so it only runs once per session)
# ─────────────────────────────────────────────

@st.cache_resource(show_spinner="Building policy index (one-time)...")
def get_rag_engine():
    engine = RAGEngine()
    engine.build_index(DOCUMENTS)
    return engine

engine = get_rag_engine()

# ─────────────────────────────────────────────
# CHAT HISTORY
# ─────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📎 Retrieved policy sources", expanded=False):
                for src in msg["sources"]:
                    st.markdown(
                        f"**[{src['doc_id']}] {src['doc_title']}** "
                        f"_(relevance: {src['score']:.2f})_\n\n> {src['text'][:300]}..."
                    )

# ─────────────────────────────────────────────
# QUERY INPUT
# ─────────────────────────────────────────────

query = st.chat_input("Ask a regulatory or policy question...")

if query:
    if not github_token:
        st.error("Please enter your GitHub Token in the sidebar to proceed.")
        st.stop()

    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Retrieve relevant chunks
    with st.spinner("Searching policy documents..."):
        retrieved = engine.retrieve(query, top_k=top_k)

    # Build RAG prompt
    rag_prompt = build_prompt(query, retrieved)

    # Call LLM via GitHub Copilot API Gateway
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            client = OpenAI(
                api_key  = github_token,
                base_url = COPILOT_BASE_URL,
                default_headers = {
                    "Editor-Version"       : "vscode/1.85.0",
                    "Editor-Plugin-Version": "copilot-chat/0.12.0",
                    "Copilot-Integration-Id": "vscode-chat",
                },
            )

            stream = client.chat.completions.create(
                model       = selected_model,
                temperature = temperature,
                stream      = True,
                messages    = [
                    {
                        "role"   : "system",
                        "content": (
                            "You are a precise regulatory compliance assistant for a bank. "
                            "Answer only from the provided policy excerpts. "
                            "Be professional and cite sources."
                        ),
                    },
                    {"role": "user", "content": rag_prompt},
                ],
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

            # Show sources inline
            with st.expander("📎 Retrieved policy sources", expanded=False):
                for i, src in enumerate(retrieved, 1):
                    st.markdown(
                        f"**[Source {i}] [{src['doc_id']}] {src['doc_title']}** "
                        f"_(relevance: {src['score']:.2f})_"
                    )
                    st.markdown(f"> {src['text'][:400]}...")
                    st.divider()

            # Show model used
            st.caption(f"Model: {selected_model_label} · Chunks retrieved: {len(retrieved)}")

        except Exception as e:
            full_response = f"❌ Error calling LLM: {str(e)}"
            response_placeholder.error(full_response)

    # Save to history
    st.session_state.messages.append({
        "role"   : "assistant",
        "content": full_response,
        "sources": retrieved,
    })

# ─────────────────────────────────────────────
# SAMPLE QUESTIONS (shown when chat is empty)
# ─────────────────────────────────────────────

if not st.session_state.messages:
    st.divider()
    st.subheader("💡 Try asking...")
    sample_questions = [
        "What CIBIL score is required for a home loan?",
        "When must an STR be filed with FIU-IND?",
        "What documents are needed for KYC of a corporate customer?",
        "What happens if a customer doesn't complete Re-KYC?",
        "Can customer data be used for AI model training?",
        "Who approves loans above INR 1 crore?",
        "What is the zero liability policy for fraud?",
    ]
    cols = st.columns(2)
    for i, q in enumerate(sample_questions):
        with cols[i % 2]:
            st.markdown(f"- *{q}*")
