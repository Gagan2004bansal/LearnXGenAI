import streamlit as st
from rag_pipeline import (
    load_pdf, 
    chunk_documents,
    store_in_pinecone, 
    ask_question
)

st.title("PDF Chatbot")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    docs = load_pdf(uploaded_file.name)
    chunks = create_chunks(docs)

    store_in_pinecone(chunks)

    st.success("PDF Indexed Successfully")

question = st.text_input("Ask Question")

if question:

    answer = ask_question(question)

    st.write(answer)