from langchain_openai import OpenAIEmbeddings
from dotnev import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(models=["text-embedding-3-large"], dimensions=32)

result = embeddings = embedding.embed_query("Delhi is the capital of India")

print(str(result))