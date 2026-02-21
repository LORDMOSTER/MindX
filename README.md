# MindX — AI Document Assistant
A professional, streamlined AI companion that transforms documents into interactive conversations and generates elite technical questions.

## Features
- **Multi-Format Upload**: Process PDFs, Word documents (.docx), and text files (.txt).
- **Hard Question Generation**: Automatically creates 35+ senior-level technical questions from your document.
- **Intelligent Q&A**: Ask deep questions and get answers grounded in the document context.
- **SaaS Interface**: Modern, professional dark-theme UI designed for productivity.
- **Local & Private**: Runs entirely on your machine using Ollama.

---

## 🛠️ Local Setup Instructions

### 1. Prerequisites
- **Python 3.12** recommended.
- **Ollama** installed and running (requires `llama3` and `nomic-embed-text` models).

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Locally
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

## ☁️ Deployment (Cloud Hosting)

To host MindX online (e.g., Streamlit Community Cloud), follow these steps:

### 1. Host the Backend
The backend (FastAPI) needs to be reachable by a public URL. 
- You can use services like **Render**, **Railway**, or **Fly.io**.
- Ensure the backend has access to an LLM (either via a hosted Ollama instance or by switching the code to use an API like OpenAI/Groq).

### 2. Host the Frontend on Streamlit Cloud
1. Push your code to a GitHub repository.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **"New app"** and select your repository.
4. **Main file path**: `frontend/app.py`
5. **Advanced Settings**:
   - Add a Secret/Environment Variable:
     ```
     MINDX_API_URL = "https://your-backend-url.com"
     ```

### 3. Deployment Note (Important)
Streamlit Community Cloud is for the UI. To make the backend work in the cloud without local Ollama:
1. **Set up a Cloud AI Provider**: 
   - Get a free API key from [Groq](https://console.groq.com/) (recommended for speed) or [OpenAI](https://platform.openai.com/).
2. **Configure Environment Variables**:
   - In your backend hosting service (Render/Railway), add:
     - `GROQ_API_KEY` = your_key
     - (Optional) `OPENAI_API_KEY` = your_key
3. **Hybrid Logic**: MindX will automatically detect these keys and switch to Cloud AI. If no keys are present, it will try to use local Ollama.
