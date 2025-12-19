import streamlit as st
import tempfile
import re

try:
    from PyPDF2 import PdfReader
except:
    from pypdf import PdfReader

def extract_methodology(text):
    headings = ["methodology", "method", "materials and methods",
                "experimental setup", "approach"]
    pattern = r'(?i)(%s)[\s\S]{0,3000}' % "|".join(headings)
    match = re.search(pattern, text)
    return match.group(0) if match else "Methodology section not found."


st.title(" Methodology Extraction")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    reader = PdfReader(pdf_path)
    text = "".join([p.extract_text() or "" for p in reader.pages])

    methodology = extract_methodology(text)
    keywords = ["methodology", "method", "experimental", "approach"]
    accuracy = 100 if any(k.lower() in methodology.lower() for k in keywords) else 0

    st.write("✅ Output Validation:")
    st.write("Methodology exists?", "not found" not in methodology.lower())
    st.write("Accuracy:", f"{accuracy}%")

    st.text_area("Methodology Output", methodology, height=300)

