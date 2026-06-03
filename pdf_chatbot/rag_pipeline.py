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
def store_in_pinecone(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview"
    )

    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name="pdf-chatbot"
    )

# Retriever 
def get_retriever():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview"
    )

    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings
    )
    
    return vector_store.as_retriever(
        search_kwargs={"k": 5}
    )

def get_rag_chain():
    retriever = get_retriever()

    prompt = PromptTemplate(
    template="""
        You are a helpful assistant. Use the following retrieved context to answer the question.
        If you don't know the answer, say you don't know.
        Context: {context}
        Question: {question}
        """,
        input_variables=["context", "question"],
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question")
        }
        | prompt | llm | StrOutputParser()
    )

    return chain


def ask_question(question):
    chain = get_rag_chain()
    response = chain.invoke({"question": question})
    return response

if __name__ == "__main__":
   
    pdf_path = "data/Gagan_Bansal_CSE26.pdf"
    documents = load_pdf(pdf_path)
    chunks = create_chunk(documents)
    store_in_pinecone(chunks)

    question = "What is the main topic of the PDF?"
    answer = ask_question(question)
    print(answer)