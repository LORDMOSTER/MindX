import os                       # Handles file paths and creating folders on your computer
import shutil                   # Used to save the uploaded file from the web to your local disk
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # Defines the "shape" of data coming from the user
from typing import List, Optional
import pdfplumber               # Specialist tool for reading and extracting text from PDF files
import docx                     # Specialist tool for reading and extracting text from Word (.docx) files
from langchain_text_splitters import RecursiveCharacterTextSplitter # Cuts long documents into manageable pieces
from langchain_community.vectorstores import Chroma                 # Library that stores document as math vectors
from langchain_ollama import OllamaEmbeddings, OllamaLLM           # Connects to Ollama models (nomic-embed and llama3)
import chromadb                 # Database engine used for ultra-fast document searching

app = FastAPI(title="MindX API")

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Initialization & Folder Setup ---
# Preparation of workspace before files are uploaded
UPLOAD_DIR = "uploads"
DB_DIR = "db"
for d in [UPLOAD_DIR, DB_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

# --- Extraction Router ---
# Looks at file extension and decides how to read it
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
        return text.strip()
    except Exception as e:
        print(f"--- Error: PDF extraction failed: {str(e)} ---")
        return ""

def extract_text_from_docx(docx_path: str) -> str:
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"--- Error: Word doc extraction failed: {str(e)} ---")
        return ""

def extract_text_from_txt(txt_path: str) -> str:
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text.strip()
    except Exception as e:
        print(f"--- Error: Text file read failed: {str(e)} ---")
        return ""

def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        return ""

# --- Text Chunking (The Scissors) ---
# Cuts long text into 1500-char segments with 300-char overlap
def chunk_text(text: str, chunk_size: int = 1500, chunk_overlap: int = 300):
    if not text:
        return []
        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return [c.strip() for c in chunks if c.strip()]

# --- AI & Memory Initialization ---
# Connects the Brain (Ollama) to the Memory (Vector Store)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
persistent_client = chromadb.PersistentClient(path=DB_DIR)
vector_store = Chroma(
    client=persistent_client,
    collection_name="mindx_collection",
    embedding_function=embeddings,
)
llm = OllamaLLM(model="llama3", temperature=0.7)

class QueryRequest(BaseModel):
    question: str
    context_source: Optional[str] = None

class QuestionGenRequest(BaseModel):
    filename: str

# --- API Endpoints (The Routes) ---
# Specific tasks the backend performs on request

@app.post("/upload") # Handles file uploads, extraction, and embedding
async def upload_document(file: UploadFile = File(...)):
    allowed_extensions = [".pdf", ".docx", ".txt"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail="Only PDF, DOCX, and TXT files are supported."
        )
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        raw_text = extract_text(file_path)
        if len(raw_text) < 100:
            raise HTTPException(status_code=400, detail="No readable text found in document or content too short.")
            
        chunks = chunk_text(raw_text)
        metadatas = [{"source": file.filename} for _ in chunks]
        vector_store.add_texts(texts=chunks, metadatas=metadatas)
        
        return {"filename": file.filename, "chunks_count": len(chunks)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/query") # Handles chat questions by finding relevant segments
async def query_document(request: QueryRequest):
    try:
        results = vector_store.similarity_search(
            request.question, 
            k=4, 
            filter={"source": request.context_source} if request.context_source else None
        )
        context = "\n".join([doc.page_content for doc in results])
        
        prompt = f"""
        You are MindX, a professional AI document assistant.
        Provide a deep, technical, and accurate answer based on the context.
        Context: {context}
        Question: {request.question}
        Answer:
        """
        return {"answer": llm.invoke(prompt)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-questions") # Generates 35+ hard engineering questions
async def generate_questions(request: QuestionGenRequest):
    try:
        # Retrieve a large amount of context for question generation
        # We'll take top 10 chunks to get a good overview
        results = vector_store.similarity_search(
            "Give me the core technical concepts and implementation details", 
            k=10, 
            filter={"source": request.filename}
        )
        context = "\n".join([doc.page_content for doc in results])
        
        prompt = f"""
        You are an elite Senior Principal Engineer. 
        Your task is to generate 35 extremely difficult, advanced technical questions based on the provided document content.
        
        The questions must target:
        - Deep technical internals and architecture
        - Scalability, performance, and security trade-offs
        - Edge cases, failure scenarios, and algorithmic complexity
        - Hard implementation challenges and debugging scenarios
        
        FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS (Markdown):
        
        # MindX — Advanced Technical Questions
        
        ## Document: {request.filename}
        
        ### Section: Core Concepts & Internals
        [List 7 questions here]
        
        ### Section: Implementation & Coding Logic
        [List 7 questions here]
        
        ### Section: Architecture & Scalability
        [List 7 questions here]
        
        ### Section: Edge Cases & Reliability
        [List 7 questions here]
        
        ### Section: Security & Performance Trade-offs
        [List 7 questions here]
        
        RULES:
        - DO NOT provide answers.
        - Questions must require deep reasoning, not simple lookups.
        - Style: Tough, interview-like, academic, and professional.
        
        Document Context:
        {context}
        """
        
        response = llm.invoke(prompt)
        return {"questions_markdown": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
