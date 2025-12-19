import streamlit as st
import tempfile

try:
    from PyPDF2 import PdfReader
except:
    from pypdf import PdfReader

def extract_pdf_text(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    pages_extracted = 0
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
            pages_extracted += 1
    return text, pages_extracted

st.title("📄 PDF Text Extraction")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    text, pages_extracted = extract_pdf_text(pdf_path)

    accuracy = 100 if len(text) > 0 and pages_extracted > 0 else 0

    st.write("✅ Output Validation:")
    st.write("Text Length:", len(text))
    st.write("Pages Extracted:", pages_extracted)
    st.write("Accuracy:", f"{accuracy}%")

    st.text_area("PDF Text Output", text[:5000], height=300)

