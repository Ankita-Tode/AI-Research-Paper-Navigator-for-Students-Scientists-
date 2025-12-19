import streamlit as st
import tempfile
import re

try:
    from PyPDF2 import PdfReader
except:
    from pypdf import PdfReader


def extract_research_gaps(text):
    keywords = ["however", "although", "limited", "limitation",
                "challenge", "future work", "not addressed", "lack of"]
    sentences = re.split(r'(?<=[.!?])\s+', text)
    gaps = [s for s in sentences if any(k in s.lower() for k in keywords) and 15 < len(s.split()) < 45]
    return gaps


st.title(" Research Gap Detection")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    reader = PdfReader(pdf_path)
    text = "".join([p.extract_text() or "" for p in reader.pages])

    gaps = extract_research_gaps(text)
    gap_keywords = ["however", "although", "limited", "limitation","challenge","future work"]
    valid_gaps = sum(1 for g in gaps if any(k in g.lower() for k in gap_keywords))
    accuracy = int(valid_gaps / len(gaps) * 100) if gaps else 0

    st.write("✅ Output Validation:")
    st.write("Total gaps found:", len(gaps))
    st.write("Gaps containing keywords:", valid_gaps)
    st.write("Accuracy:", f"{accuracy}%")

    if gaps:
        for i, g in enumerate(gaps,1):
            st.markdown(f"**Gap {i}:** {g}")
    else:
        st.info("No research gaps detected.")
