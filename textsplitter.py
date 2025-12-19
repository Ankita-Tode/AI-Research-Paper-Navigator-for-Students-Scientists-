import streamlit as st
import tempfile
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter

try:
    from PyPDF2 import PdfReader
except:
    from pypdf import PdfReader


def split_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    return splitter.split_text(text)

st.title(" PDF Text Splitter")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    reader = PdfReader(pdf_path)
    text = "".join([p.extract_text() or "" for p in reader.pages])

    chunks = split_text(text)
    chunk_lengths = [len(c) for c in chunks]

    valid_length_count = sum(1 for l in chunk_lengths if 850 <= l <= 1150)
    accuracy = int(valid_length_count / len(chunks) * 100) if chunks else 0

    st.write("✅ Output Validation:")
    st.write("Total Chunks:", len(chunks))
    st.write("Chunks with length 850-1150 chars:", valid_length_count)
    st.write("Accuracy:", f"{accuracy}%")

    st.subheader("Sample Chunks Preview")
    for i, chunk in enumerate(chunks[:3], 1):
        st.text_area(f"Chunk {i}", chunk, height=200)
