
# Project Notes

## 1. Overview

Build a LLM-powered chat application that can answer questions from documents (for example, PDFs).

**Future scope:** Support additional document types (Word, HTML, images/OCR, etc.).

## 2. Input

- Documents are provided at runtime (user upload or ingestion pipeline).

## 3. Data persistence

- In-memory for prototyping; persist indexes/embeddings to external storage for production.

## 4. Requirements

- Users can upload a PDF (or multiple PDFs).
- Users can request a summary of a document.
- Users can ask for details present in the document (fact-based QA).
- Users can ask follow-up questions (conversation/chain-of-thought support).

## 5. Tech stack

1. OpenAI (or other LLM provider) — LLM inference
2. LangGraph — semantic search/orchestration (as written)
3. Chroma DB — vector database (or alternative: FAISS, Milvus, pgvector)

**Later / optional components**

- FastAPI — backend API
- React — frontend UI








