import streamlit as st
import os

from rag_pipeline import (
    load_pdf,
    create_chunk,
    store_in_pinecone,
    ask_question
)

# TITLE
st.title("PDF Chatbot")


# INITIALIZE SESSION STATE
os.makedirs("data", exist_ok=True)
pdf_files = [
    f for f in os.listdir("data")
    if f.endswith(".pdf")
]

# UPLOAD PDF
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:
    namespace = uploaded_file.name

    if namespace not in pdf_files:

        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        docs = load_pdf(file_path)
        chunks = create_chunk(docs)
        store_in_pinecone(chunks, namespace)

        st.success(f"{namespace} Indexed Successfully")
        st.rerun()

# DROPDOWN TO SELECT PDF
selected_pdf = st.selectbox(
    "Select PDF",
    options=[None] + pdf_files,
    format_func=lambda x: "Choose a PDF..." if x is None else x
)

if selected_pdf:
    st.info(f"Currently querying: {selected_pdf}")


# INPUT BOX FOR QUERY
if selected_pdf:
    question = st.text_input("Ask Question")
else:
    question = st.text_input(
        "Select a PDF first",
        disabled=True
    )

if question and selected_pdf:

    with st.spinner("Searching PDF and generating answer..."):
        result = ask_question(
            question, 
            selected_pdf
        )

    st.write("### Answer")
    st.write(result["answer"])

    st.caption(
        f"Sources: {', '.join(result['sources'])}"
    )
