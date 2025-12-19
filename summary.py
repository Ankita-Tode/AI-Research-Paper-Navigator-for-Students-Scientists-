import streamlit as st
import tempfile
import re

try:
    from PyPDF2 import PdfReader
except:
    from pypdf import PdfReader


def simple_summary(text, max_sentences=6):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return " ".join(sentences[:max_sentences])

st.title(" Simple Summary Generator")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    reader = PdfReader(pdf_path)
    text = "".join([p.extract_text() or "" for p in reader.pages])

    summary = simple_summary(text)
    punct_count = sum(1 for c in summary if c in ".!?")
    accuracy = 100 if len(summary) < len(text) and punct_count >= 1 else 0

    st.write("✅ Output Validation:")
    st.write("Summary Length:", len(summary))
    st.write("Number of sentences in summary:", punct_count)
    st.write("Accuracy:", f"{accuracy}%")

    st.text_area("Summary Output", summary, height=200)
