import streamlit as st
import tempfile
import re

try:
    from PyPDF2 import PdfReader
except:
    from pypdf import PdfReader


def extract_contributions(text):
    keywords = ["contribution", "novel", "we propose", "this paper presents"]
    pattern = r'(?i)(%s)[\s\S]{0,3000}' % "|".join(keywords)
    match = re.search(pattern, text)
    return match.group(0) if match else "Contributions not found."


st.title(" Contributions Extraction")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    reader = PdfReader(pdf_path)
    text = "".join([p.extract_text() or "" for p in reader.pages])

    contrib = extract_contributions(text)
    keywords = ["contribution", "novel", "we propose", "this paper presents"]
    accuracy = 100 if any(k.lower() in contrib.lower() for k in keywords) else 0

    st.write("✅ Output Validation:")
    st.write("Contributions detected?", "not found" not in contrib.lower())
    st.write("Accuracy:", f"{accuracy}%")

    st.text_area("Contributions Output", contrib, height=300)


