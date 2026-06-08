import streamlit as st
import os

from rag_pipeline import (
    load_pdf,
    create_chunk,
    store_in_pinecone,
    ask_question,
    delete_pdf,
    delete_all_pdfs
)

# TITLE
st.title("MULTI PDF Chatbot")

# CHAT HISTORY 
if "messages" not in st.session_state:
    st.session_state.messages = []


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
selected_pdfs = st.multiselect(
    "Select PDF(s)",
    options=pdf_files
)

# SEARCH ALL PDFS
search_all = st.checkbox(
    "Search All PDFs"
)

if search_all:
    selected_pdfs = pdf_files

# TRACK CURRENT PDF
if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None

# CLEAR CHAT IF PDF CHANGES
current_selection = tuple(
    sorted(selected_pdfs)
)

if "current_pdfs" not in st.session_state:
    st.session_state.current_pdfs = ()

if current_selection != st.session_state.current_pdfs:

    st.session_state.messages = []

    st.session_state.current_pdfs = current_selection


if search_all:
    st.info("Currently querying: All PDFs")
if selected_pdfs:
    st.info(
        f"Currently querying: {', '.join(selected_pdfs)}"
    )


# DELETE PDF FROM PINECONE AND LOCAL STORAGE
if len(selected_pdfs) == 1:

    selected_pdf = selected_pdfs[0]

    if st.button(
        f"Delete {selected_pdf}"
    ):

        delete_pdf(selected_pdf)

        file_path = os.path.join(
            "data",
            selected_pdf
        )

        if os.path.exists(file_path):
            os.remove(file_path)

        st.success(
            f"{selected_pdf} deleted"
        )

        st.rerun()

## DELETE BUTTON 
if st.button(
    "Delete All PDFs"
):

    delete_all_pdfs()

    for pdf in pdf_files:

        os.remove(
            os.path.join(
                "data",
                pdf
            )
        )

    st.success(
        "All PDFs deleted"
    )

    st.rerun()

# CLEAR CHAT HISTORY BUTTON
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# INPUT BOX FOR QUERY
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

    
if selected_pdfs:
    question = st.chat_input(
        "Ask a question"
    )
else:
    question = st.text_input(
        "Select a PDF first",
        disabled=True
    )


if question and selected_pdfs:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.spinner("Searching PDF and generating answer..."):
        result = ask_question(
            question, 
            selected_pdfs,
            st.session_state.messages
        )

    with st.chat_message("assistant"):
        st.write(result["answer"])

        st.caption(
            f"Sources: {', '.join(result['sources'])}, Similarity Score: {result['similarity_score']}, Answer found in {result['relevant_sections']} relevant sections of the document."
        )
        

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"]
    })

    
