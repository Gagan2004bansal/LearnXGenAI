import os 
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings)
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


# Load PDF 
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents

# Split text into chunks
def create_chunk(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200   
    )
    return splitter.split_documents(documents)

# Store chunks in Pinecone
def store_in_pinecone(chunks, namespace):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview"
    )

    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME,
        namespace=namespace
    )

# Retriever 
def get_retriever(namespace):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview"
    )

    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
        namespace=namespace
    )
    
    return vector_store.as_retriever(
        search_kwargs={"k": 5}
    )

# RAG Chain
def get_rag_chain():

    prompt = PromptTemplate(
        template="""
        You are a helpful assistant.

        Use the following context to answer the question.

        If the answer is not present in the context, say you don't know.

        Chat History:
        {chat_history}

        Context:
        {context}

        Question:
        {question}
        """,
        input_variables=["context", "question", "chat_history"],
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    chain = prompt | llm | StrOutputParser()

    return chain

# Format Docs
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Ask question
def ask_question(question, namespace, chat_history):

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview"
    )

    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
        namespace=namespace
    )

    results = vector_store.similarity_search_with_score(
        question,
        k=5
    )

    docs = [doc for doc, score in results]
    scores = [score for doc, score in results]

    avg_score = round(sum(scores) / len(scores), 3)

    context = format_docs(docs)

    history_text = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in chat_history
        ]
    )

    chain = get_rag_chain()

    answer = chain.invoke({
        "chat_history": history_text,
        "context": context,
        "question": question
    })

    sources = []

    for doc in docs:
        page = doc.metadata.get("page")

        if page is not None:
            sources.append(f"Page {page + 1}")

    return {
        "answer": answer,
        "sources": sorted(list(set(sources))),
        "similarity_score": avg_score
    }

# Testing the pipeline
# if __name__ == "__main__":
   
#     pdf_path = "data/Gagan_Bansal_CSE26.pdf"
#     documents = load_pdf(pdf_path)
#     chunks = create_chunk(documents)
#     store_in_pinecone(chunks)

#     question = "What is the main topic of the PDF?"
#     answer = ask_question(question)
#     print(answer)