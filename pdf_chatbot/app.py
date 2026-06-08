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

# CHAT HISTORY 
if "messages" not in st.session_state:
    st.session_state.messages = []

# CLEAR CHAT HISTORY
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

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

# TRACK CURRENT PDF
if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None

# CLEAR CHAT IF PDF CHANGES
if ( selected_pdf and selected_pdf != st.session_state.current_pdf ):

    st.session_state.messages = []

    st.session_state.current_pdf = selected_pdf

if selected_pdf:
    st.info(f"Currently querying: {selected_pdf}")


# INPUT BOX FOR QUERY
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

    
if selected_pdf:
    question = st.chat_input(
        "Ask a question"
    )
else:
    question = st.text_input(
        "Select a PDF first",
        disabled=True
    )


if question and selected_pdf:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.spinner("Searching PDF and generating answer..."):
        result = ask_question(
            question, 
            selected_pdf,
            st.session_state.messages
        )

    with st.chat_message("assistant"):
        st.write(result["answer"])

        st.caption(
            f"Sources: {', '.join(result['sources'])}"
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"]
    })

    
