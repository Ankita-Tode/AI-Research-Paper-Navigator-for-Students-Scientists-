
import re
import tempfile
from typing import List

import streamlit as st

# ============================
# SAFE PDF IMPORT (NO CRASH)
# ============================

PdfReader = None
pdf_backend = None

try:
    from PyPDF2 import PdfReader
    pdf_backend = "PyPDF2"
except ModuleNotFoundError:
    try:
        from pypdf import PdfReader
        pdf_backend = "pypdf"
    except ModuleNotFoundError:
        PdfReader = None

# ============================
# LangChain imports (NO LLM)
# ============================
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


# ============================
# PDF TEXT EXTRACTION
# ============================

def extract_pdf_text(pdf_path: str) -> str:
    if PdfReader is None:
        return ""

    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


# ============================
# TEXT SPLITTING (LangChain)
# ============================

def split_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    return splitter.split_text(text)


# ============================
# SIMPLE EXTRACTIVE SUMMARY (NO LLM)
# ============================

def simple_summary(text: str, max_sentences: int = 6) -> str:
    sentences = re.split(r'(?<=[.!?]) +', text)
    return " ".join(sentences[:max_sentences])


# ============================
# RULE-BASED SECTION FINDING
# ============================

def find_section(text: str, keywords: List[str], limit: int = 2000) -> str:
    lower = text.lower()
    for kw in keywords:
        idx = lower.find(kw)
        if idx != -1:
            return text[idx:idx + limit]
    return "Section not clearly found."


# ============================
# STREAMLIT UI
# ============================

st.set_page_config(page_title="Offline Research Paper Reader", layout="wide")

st.title("📄 Offline Research Paper Reader (LangChain – No API Key)")

if PdfReader is None:
    st.error(
        "PDF library not found. Please install ONE of the following and restart:\n\n"
        "pip install PyPDF2\n"
        "OR\n"
        "pip install pypdf"
    )
    st.stop()

st.success(f"Using PDF backend: {pdf_backend}")

uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type=["pdf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    with st.spinner("Reading PDF..."):
        full_text = extract_pdf_text(pdf_path)

    if not full_text.strip():
        st.error("Could not extract text. PDF may be scanned (image-based).")
        st.stop()

    chunks = split_text(full_text)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "📘 Easy Summary",
        "🧪 Methodology",
        "✨ Key Contributions",
        "📚 Semantic Search"
    ])

    with tab1:
        st.subheader("Easy (Extractive) Summary")
        st.write(simple_summary(full_text))

    with tab2:
        st.subheader("Methodology (Extracted)")
        st.write(find_section(full_text, ["methodology", "methods"]))

    with tab3:
        st.subheader("Likely Contributions")
        st.write(find_section(full_text, ["contribution", "proposed", "novel"]))

    with tab4:
        st.subheader("Semantic Similarity Search (Local)")
        query = st.text_input("Enter a topic to search inside the paper")
        if query:
            results = vectordb.similarity_search(query, k=3)
            for i, r in enumerate(results, 1):
                st.markdown(f"**Result {i}:**")
                st.write(r.page_content)

else:
    st.info("Please upload a research paper PDF to begin.")



