"""
WHO PDF RAG Query System - Streamlit App
=========================================

A beautiful web interface for querying PDF documents using RAG.
Deploy on streamlit.io or run locally with: streamlit run streamlit_app.py

Author: Enhanced RAG System
Date: December 2024
"""

import streamlit as st
import os
import tempfile
from datetime import datetime
from typing import Optional, List, Dict, Any

# Import RAG components
try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_groq import ChatGroq
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
    from langchain_core.prompts import ChatPromptTemplate
except ImportError as e:
    st.error(f"❌ Missing required package: {e}")
    st.info("Please install: pip install langchain langchain-community langchain-groq langchain-huggingface faiss-cpu pypdf sentence-transformers")
    st.stop()


# Page config
st.set_page_config(
    page_title="WHO PDF RAG System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .source-badge {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        margin: 0.2rem;
        background-color: #fff3cd;
        border-radius: 0.3rem;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


class StreamlitRAGSystem:
    """RAG system optimized for Streamlit."""
    
    @staticmethod
    @st.cache_resource(show_spinner=False)
    def load_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
        """Load and cache the embedding model."""
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    @staticmethod
    def process_pdf(pdf_file, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Process uploaded PDF file."""
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            # Load PDF
            loader = PyPDFLoader(tmp_path)
            raw_docs = loader.load()
            
            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", ". ", " ", ""]
            )
            
            docs = text_splitter.split_documents(raw_docs)
            
            return docs, len(raw_docs)
            
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    @staticmethod
    def create_vectorstore(docs, embedding_model):
        """Create FAISS vector store."""
        return FAISS.from_documents(docs, embedding_model)
    
    @staticmethod
    def create_rag_chain(vectorstore, api_key: str, temperature: float = 0.0):
        """Create the RAG chain."""
        # Create retriever
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.5}
        )
        
        # Initialize LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            max_tokens=1024,
            api_key=api_key
        )
        
        # Create prompt
        system_prompt = (
            "You are an expert medical AI assistant analyzing PDF documents. "
            "Your role is to provide accurate, well-sourced answers based on the document.\n\n"
            
            "INSTRUCTIONS:\n"
            "1. Use ONLY the provided context to answer questions\n"
            "2. Always cite page numbers when referencing information (e.g., [Page 12])\n"
            "3. If information is not in the context, clearly state: 'I cannot find that information in the provided PDF.'\n"
            "4. Be concise but comprehensive\n"
            "5. Use professional terminology when appropriate\n"
            "6. If context is ambiguous or contradictory, acknowledge this\n\n"
            
            "CONTEXT:\n{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        # Build chain
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        return rag_chain


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'rag_chain' not in st.session_state:
        st.session_state.rag_chain = None
    
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
    
    if 'pdf_name' not in st.session_state:
        st.session_state.pdf_name = None
    
    if 'num_pages' not in st.session_state:
        st.session_state.num_pages = 0
    
    if 'num_chunks' not in st.session_state:
        st.session_state.num_chunks = 0


def sidebar():
    """Render sidebar with settings and file upload."""
    with st.sidebar:
        st.markdown("### 📚 WHO PDF RAG System")
        st.markdown("---")
        
        # API Key input
        st.markdown("#### 🔑 API Configuration")
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Get your free API key at console.groq.com",
            value=os.environ.get("GROQ_API_KEY", "")
        )
        
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key
        
        st.markdown("---")
        
        # File upload
        st.markdown("#### 📄 Upload PDF")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a WHO report or any PDF document"
        )
        
        st.markdown("---")
        
        # Advanced settings
        with st.expander("⚙️ Advanced Settings"):
            chunk_size = st.slider(
                "Chunk Size",
                min_value=200,
                max_value=2000,
                value=1000,
                step=100,
                help="Size of text chunks for processing"
            )
            
            chunk_overlap = st.slider(
                "Chunk Overlap",
                min_value=0,
                max_value=500,
                value=200,
                step=50,
                help="Overlap between chunks for context continuity"
            )
            
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.1,
                help="0 = factual, 1 = creative"
            )
        
        # Process PDF button
        if uploaded_file and api_key:
            if st.button("🚀 Process PDF", type="primary", use_container_width=True):
                process_pdf_file(uploaded_file, api_key, chunk_size, chunk_overlap, temperature)
        elif uploaded_file and not api_key:
            st.warning("⚠️ Please enter your Groq API key first")
        
        # Status
        st.markdown("---")
        st.markdown("#### 📊 Status")
        if st.session_state.pdf_processed:
            st.success("✅ PDF Processed")
            st.info(f"**File:** {st.session_state.pdf_name}")
            st.info(f"**Pages:** {st.session_state.num_pages}")
            st.info(f"**Chunks:** {st.session_state.num_chunks}")
        else:
            st.info("💡 Upload and process a PDF to start")
        
        # Clear button
        if st.session_state.pdf_processed:
            if st.button("🗑️ Clear & Reset", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        
        st.markdown("---")
        st.markdown("#### ℹ️ About")
        st.markdown("""
        This app uses:
        - **LangChain** for RAG
        - **FAISS** for vector search
        - **Groq + Llama 3.3** for answers
        - **HuggingFace** for embeddings
        """)
        
        st.markdown("---")
        st.markdown("Made with ❤️ for WHO PDF analysis")


def process_pdf_file(uploaded_file, api_key: str, chunk_size: int, chunk_overlap: int, temperature: float):
    """Process the uploaded PDF and create RAG chain."""
    with st.spinner("📖 Processing PDF..."):
        try:
            # Process PDF
            progress_bar = st.progress(0, text="Loading PDF...")
            docs, num_pages = StreamlitRAGSystem.process_pdf(
                uploaded_file,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            progress_bar.progress(33, text=f"Loaded {num_pages} pages, created {len(docs)} chunks")
            
            # Load embeddings
            progress_bar.progress(40, text="Loading embedding model...")
            embedding_model = StreamlitRAGSystem.load_embedding_model()
            
            # Create vector store
            progress_bar.progress(50, text="Creating vector database...")
            vectorstore = StreamlitRAGSystem.create_vectorstore(docs, embedding_model)
            progress_bar.progress(75, text="Vector database created")
            
            # Create RAG chain
            progress_bar.progress(85, text="Setting up RAG chain...")
            rag_chain = StreamlitRAGSystem.create_rag_chain(
                vectorstore,
                api_key,
                temperature=temperature
            )
            progress_bar.progress(100, text="Complete!")
            
            # Update session state
            st.session_state.rag_chain = rag_chain
            st.session_state.pdf_processed = True
            st.session_state.pdf_name = uploaded_file.name
            st.session_state.num_pages = num_pages
            st.session_state.num_chunks = len(docs)
            st.session_state.messages = []
            
            progress_bar.empty()
            st.success(f"✅ Successfully processed {uploaded_file.name}")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")
            if "api" in str(e).lower():
                st.info("💡 Please check your Groq API key")


def display_chat_message(role: str, content: str, sources: Optional[List[int]] = None):
    """Display a chat message with styling."""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 Assistant:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
        
        if sources:
            sources_html = " ".join([
                f'<span class="source-badge">📄 Page {s}</span>'
                for s in sorted(set(sources))
            ])
            st.markdown(f"""
            <div style="margin-top: 0.5rem;">
                <strong>Sources:</strong> {sources_html}
            </div>
            """, unsafe_allow_html=True)


def query_rag_system(question: str):
    """Query the RAG system and return response."""
    try:
        with st.spinner("🤔 Thinking..."):
            response = st.session_state.rag_chain.invoke({"input": question})
            
            answer = response.get("answer", "No answer generated")
            
            # Extract sources
            sources = []
            if "context" in response:
                for doc in response["context"]:
                    page = doc.metadata.get('page', None)
                    if page:
                        sources.append(page)
            
            return answer, sources
            
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        if "rate limit" in str(e).lower():
            error_msg += "\n\n💡 You may have hit the API rate limit. Please wait a moment."
        elif "api key" in str(e).lower():
            error_msg += "\n\n💡 Please check your API key."
        return error_msg, []


def main():
    """Main application."""
    initialize_session_state()
    sidebar()
    
    # Main content
    st.markdown('<div class="main-header">📚 WHO PDF Query System</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Ask questions about your PDF documents using AI-powered RAG</div>',
        unsafe_allow_html=True
    )
    
    # Instructions or chat interface
    if not st.session_state.pdf_processed:
        st.info("👈 **Get Started:** Upload a PDF and enter your Groq API key in the sidebar")
        
        # Show example questions
        st.markdown("### 💡 Example Questions You Can Ask:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            - What is the executive summary?
            - What are the main findings?
            - What criteria are mentioned?
            - Summarize the key recommendations
            """)
        
        with col2:
            st.markdown("""
            - Which organizations are mentioned?
            - What are the main challenges?
            - What methodologies were used?
            - List the key statistics
            """)
        
        # Features
        st.markdown("---")
        st.markdown("### ✨ Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🎯 Accurate")
            st.markdown("Citations with page numbers for every answer")
        
        with col2:
            st.markdown("#### ⚡ Fast")
            st.markdown("Powered by Groq's lightning-fast inference")
        
        with col3:
            st.markdown("#### 🔒 Private")
            st.markdown("Embeddings run locally, secure processing")
        
    else:
        # Chat interface
        st.markdown("### 💬 Chat with Your Document")
        
        # Display chat history
        for message in st.session_state.messages:
            display_chat_message(
                message["role"],
                message["content"],
                message.get("sources")
            )
        
        # Chat input
        if question := st.chat_input("Ask a question about the PDF..."):
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": question
            })
            display_chat_message("user", question)
            
            # Get response
            answer, sources = query_rag_system(question)
            
            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
            display_chat_message("assistant", answer, sources)
        
        # Quick actions
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📋 Summarize Document", use_container_width=True):
                question = "Provide a comprehensive summary of this document including its main purpose, key findings, and conclusions."
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()
        
        with col2:
            if st.button("🎯 Key Points", use_container_width=True):
                question = "What are the most important key points and takeaways from this document?"
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()
        
        with col3:
            if st.button("📊 Statistics", use_container_width=True):
                question = "List all important statistics, numbers, and quantitative data mentioned in the document."
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()
        
        with col4:
            if st.button("✅ Recommendations", use_container_width=True):
                question = "What are the main recommendations or action items suggested in this document?"
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()


if __name__ == "__main__":
    main()
