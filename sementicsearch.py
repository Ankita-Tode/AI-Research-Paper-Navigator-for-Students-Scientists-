import streamlit as st
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

try:
    from PyPDF2 import PdfReader
except:
    from pypdf import PdfReader

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    return splitter.split_text(text)


st.title(" Semantic Search (Local)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
query = st.text_input("Enter search query")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    reader = PdfReader(pdf_path)
    text = "".join([p.extract_text() or "" for p in reader.pages])

    chunks = split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_texts(chunks, embeddings)

    st.success("Semantic search ready")

    if query:
        results = vectordb.similarity_search(query, k=3)
        valid_results = sum(1 for r in results if any(q.lower() in r.page_content.lower() for q in query.split()))
        accuracy = int(valid_results / len(results) * 100) if results else 0

        st.write("✅ Output Validation:")
        st.write("Results returned:", len(results))
        st.write("Results containing query words:", valid_results)
        st.write("Accuracy:", f"{accuracy}%")

        for i, r in enumerate(results,1):
            st.markdown(f"**Result {i}:**")
            st.write(r.page_content)
