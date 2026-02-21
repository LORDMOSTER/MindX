# MindX - AI Document Assistant

A professional, streamlined AI companion that transforms static PDFs into interactive conversations.

## Features
- **Multi-Format Upload**: Process PDFs, Word documents (.docx), text files (.txt), and images (.png, .jpg).
- **OCR Engine**: Automatically extracts text from scanned PDFs and images using Tesseract OCR.
- **Intelligent Q&A**: Ask deep questions and get answers grounded in the document context.
- **SaaS Interface**: Modern, professional dark-theme UI designed for productivity.
- **Local & Private**: Runs entirely on your machine using Ollama for total data privacy.

## Setup Instructions

### 1. Prerequisites
- Python 3.12 recommended
- [Ollama](https://ollama.com/) installed and running.
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed on your system.
  - Windows: Expected at `C:\Program Files\Tesseract-OCR\tesseract.exe`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Models
Ensure you have the required models pulled in Ollama:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### 4. Run the Application

**Option A: Using Batch Scripts (Recommended for Windows)**
- Double-click `run_backend.bat` to start the MindX API server.
- Double-click `run_frontend.bat` to start the MindX Dashboard.

**Option B: Manual Commands**
- **Start the Backend:** `uvicorn backend.main:app --reload`
- **Start the Frontend:** `streamlit run frontend/app.py`

## Project Structure
- `backend/`: FastAPI server logic (MindX API).
- `frontend/`: Streamlit UI (MindX UI).
- `uploads/`: Document storage.
- `db/`: Vector database (ChromaDB).
