---
title: RAG Document Chatbot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: true
---

# 🤖 RAG Document Chatbot

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://rag-chatbot-openai-jwdjh5few585qmnld6cgwm.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-1.x-orange)](https://langchain.com)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20Store-purple)](https://pinecone.io)

An AI-powered chatbot that answers questions about your documents — grounded in real content, not guesswork.

Built with **OpenAI GPT-4o**, **LangChain Core 1.x (LCEL)**, **Pinecone**, and **Streamlit**.

---

## 🚀 Live Demo

👉 **[Try it here](https://rag-chatbot-openai-jwdjh5few585qmnld6cgwm.streamlit.app/)**

**Demo password:** `demo2026`

This demo is pre-loaded with **Alphabet's Q1 2026 Earnings Report**. Try asking:
- *"What was Alphabet's total revenue in Q1 2026?"*
- *"What did the CEO say about AI?"*
- *"How did Google Cloud perform this quarter?"*
- *"What was the net income?"*

---

## 🎯 What It Does

Most AI chatbots answer from general training data and can make things up. This chatbot only answers from **your uploaded documents** — and tells you exactly which page the answer came from.

**Example:**

> **Q:** What did the CEO say about AI?
>
> **A:** Sundar Pichai said that 2026 is off to a terrific start and that their AI investments and full stack approach are lighting up every part of the business. He mentioned AI experiences are driving usage in Search, with queries at an all-time high and 19% revenue growth. *(Source: Page 1)*

---

## ✨ Key Features

- **Semantic Search** — Finds relevant content even when exact words don't match
- **Multi-turn Conversation** — Remembers context across follow-up questions
- **Source Citations** — Shows exactly which page each answer came from
- **Honest Responses** — Says "I don't know" when the answer isn't in the document
- **Password Protected** — Secure demo access
- **Real-time Chat UI** — Clean, interactive interface built with Streamlit

---

## 🏗️ Architecture

```
User Question
    → OpenAI Embeddings converts question to vector
    → Pinecone finds top 3 most similar document chunks
    → GPT-4o synthesizes answer from retrieved chunks
    → Streamlit displays answer + source citations
```

### Tech Stack

| Component | Technology |
|---|---|
| LLM | OpenAI GPT-4o |
| Embeddings | OpenAI text-embedding-3-small (1536 dimensions) |
| Vector Store | Pinecone (cosine similarity) |
| Orchestration | LangChain Core 1.x (LCEL) |
| UI | Streamlit |
| Language | Python 3.11 |
| Hosting | Streamlit Community Cloud |

---

## 💡 How It Works

### 1. Document Ingestion (`ingest.py`)
- Loads PDF files from the `data/` folder
- Splits documents into 1,000-character chunks with 200-character overlap
- Converts each chunk into a vector using OpenAI `text-embedding-3-small`
- Stores vectors in Pinecone for fast semantic retrieval

### 2. RAG Pipeline (`app.py`)
- Embeds the user's question using the same OpenAI embedding model
- Searches Pinecone for the 3 most semantically similar chunks
- Rewrites follow-up questions into standalone questions using chat history
- Sends retrieved chunks + question to GPT-4o
- Returns a grounded answer with page-level source citations

### 3. Multi-turn Memory
- Maintains full conversation history across exchanges
- Rewrites ambiguous follow-up questions to be standalone
- Prevents context loss between turns

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- OpenAI API key → [platform.openai.com](https://platform.openai.com)
- Pinecone API key → [pinecone.io](https://pinecone.io)

### Installation

```bash
# Clone the repo
git clone https://github.com/hanzheng0613/rag-chatbot-openai.git
cd rag-chatbot-openai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=rag-chatbot
```

### Running the App

**Step 1 — Add your PDF files to the `data/` folder**

**Step 2 — Ingest documents into Pinecone:**
```bash
python ingest.py
```

**Step 3 — Launch the chatbot:**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` and start chatting!

---

## 📁 Project Structure

```
rag-chatbot-openai/
├── data/               ← Place your PDF files here (not committed)
├── app.py              ← Streamlit UI + RAG pipeline
├── ingest.py           ← Document ingestion pipeline
├── requirements.txt    ← Python dependencies
├── .env                ← API keys (not committed to GitHub)
└── .gitignore
```

---

## 🧠 Why RAG?

| Regular ChatGPT | This RAG Chatbot |
|---|---|
| Answers from training data | Answers from your documents |
| Can hallucinate facts | Grounded in real sources |
| No citations | Shows exact page numbers |
| Knowledge cutoff | Always current with your docs |

---

## 👤 Author

**Hanzheng Wang**
- 🔗 [LinkedIn](https://www.linkedin.com/in/hanzheng-wang-072801416/)
- 🐙 [GitHub](https://github.com/hanzheng0613)
- 📧 hanzheng0613@gmail.com
