# MindX — AI Document Assistant
A professional, streamlined AI companion that transforms documents into interactive conversations, powered entirely by your local machine.

## Features
- **Multi-Format Upload**: Process PDFs, Word documents (.docx), and text files (.txt).
- **Intelligent Q&A**: Ask deep questions and get answers grounded in the document context.
- **SaaS Interface**: Modern, professional dark-theme UI designed for productivity.
- **Local & Private**: Runs entirely on your machine using Ollama for maximum data privacy.

---

## 🛠️ Local Setup Instructions

### 1. Prerequisites
- **Python 3.12** recommended.
- **Ollama** installed and running.
- **Models**: Ensure you have `llama3` and `nomic-embed-text` installed.
  ```bash
  ollama pull llama3
  ollama pull nomic-embed-text
  ```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run MindX
**Option A: Using Batch Scripts (Windows)**
1. Run `run_backend.bat` in one terminal.
2. Run `run_frontend.bat` in another terminal.

**Option B: Manual Commands**
```bash
# Terminal 1: Backend
uvicorn backend.main:app --reload

# Terminal 2: Frontend
streamlit run frontend/app.py
```

---

## 🔒 Privacy & Security
MindX is designed to be **private by default**. Your documents never leave your machine. All processing, embedding, and inference happen locally via Ollama and ChromaDB.
