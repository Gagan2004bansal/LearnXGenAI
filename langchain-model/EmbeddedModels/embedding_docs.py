from langchain_openai import OpenAIEmbeddings
from dotnev import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(models=["text-embedding-3-large"], dimensions=32)

documents = [
    "Delhi is the capital of India",
    "Mumbai is the financial capital of India",
    "Bangalore is the IT hub of India",
]

result = embeddings = embedding.embed_documents(documents)

print(str(result))