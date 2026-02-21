import streamlit as st
import requests
import os
import time

# Page configuration
st.set_page_config(
    page_title="MindX | AI Document Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for MindX SaaS Look ---
st.markdown("""
<style>
    /* Main Background and Theme */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Top Navbar Simulation */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 2rem;
        background: rgba(26, 28, 30, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    
    .nav-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #fff;
    }
    
    .nav-status {
        font-size: 0.85rem;
        padding: 4px 12px;
        border-radius: 20px;
        background: rgba(40, 167, 69, 0.1);
        color: #28a745;
        border: 1px solid rgba(40, 167, 69, 0.2);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar-logo {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-align: center;
        background: linear-gradient(90deg, #0d6efd, #6f42c1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sidebar-tagline {
        font-size: 0.9rem;
        color: #8b949e;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Message Bubbles */
    .chat-card {
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        max-width: 85%;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .user-card {
        background: #238636;
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    
    .ai-card {
        background: #21262d;
        color: #e6edf3;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Custom Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 0.75rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .main-btn>div>button {
        background: linear-gradient(90deg, #0d6efd, #00d4ff);
        color: white;
    }
    
    .main-btn>div>button:hover {
        box-shadow: 0 0 15px rgba(13, 110, 253, 0.4);
        transform: scale(1.02);
    }
    
    .secondary-btn>div>button {
        background: rgba(255, 255, 255, 0.05);
        color: #c9d1d9;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .secondary-btn>div>button:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: #6f42c1;
        color: white;
    }

    /* Hide Default Header */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Input Area Fixed Bottom */
    .stChatInput {
        padding: 2rem 5rem !important;
        background: #0e1117 !important;
    }
    
    .stChatInput > div {
        border-radius: 25px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        background: #1c2128 !important;
    }

    /* Adjustment to make space for custom header */
    .block-container {
        padding-top: 5rem;
        max-width: 950px;
    }
</style>

<div class="top-nav">
    <div class="nav-title">MindX</div>
    
</div>
""", unsafe_allow_html=True)

# --- API Configuration ---
# Use environment variable for cloud deployment, fallback to localhost for development
API_BASE_URL = os.getenv("MINDX_API_URL", "http://localhost:8000")

# --- Sidebar Content ---
with st.sidebar:
    st.markdown('<div class="sidebar-logo">MindX</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">AI Document Assistant</div>', unsafe_allow_html=True)
    
    st.subheader("⚙️ Settings")
    knowledge_scope = st.radio(
        "Knowledge Scope", 
        ["Document Only", "General AI"],
        index=0
    )
    
    st.divider()
    
    st.subheader("📁 Upload Document")
    uploaded_file = st.file_uploader(
        "PDF, DOCX, TXT only", 
        type=["pdf", "docx", "txt"], 
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.info(f"📄 {uploaded_file.name}")
        
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        if st.button("Process Document", use_container_width=True):
            with st.status("🔍 Analyzing...", expanded=True) as status:
                files = {"file": uploaded_file}
                try:
                    response = requests.post(f"{API_BASE_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.session_state["active_file"] = uploaded_file.name
                        status.update(label="Document Ready!", state="complete", expanded=False)
                        st.toast("Ready for chat & questions!")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Failed to process')}")
                except Exception as e:
                    st.error(f"Backend offline: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Main Interaction Area ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding-top: 50px;">
        <h1 style="font-size: 3.5rem; margin-bottom: 0px;">MindX</h1>
        <p style="font-size: 1.4rem; color: #8b949e; margin-bottom: 40px;">Interactive Document Assistant</p>
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; max-width: 600px; margin: 0 auto;">
            <p style="color: #c9d1d9; font-size: 1.1rem;">MindX is your elite technical companion. Upload complex documentation to chat, extract insights, and master your technical files locally.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display Messages
for message in st.session_state.messages:
    role_class = "user-card" if message["role"] == "user" else "ai-card"
    st.markdown(f"""
    <div class="chat-card {role_class}">
        {message["content"]}
    </div>
    """, unsafe_allow_html=True)

# Chat Input Area
if prompt := st.chat_input("Ask MindX anything about your document..."):
    if "active_file" not in st.session_state:
        st.warning("Please upload and process a document first.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

# Handle AI Response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant", avatar="🧠"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*(MindX is analyzing...)*")
        
        payload = {
            "question": user_prompt,
            "context_source": st.session_state["active_file"] if knowledge_scope == "Document Only" else None
        }
        
        try:
            response = requests.post(f"{API_BASE_URL}/query", json=payload)
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()
            else:
                message_placeholder.error("MindX encountered an error.")
        except Exception as e:
            message_placeholder.error(f"Connection failed: {e}")
