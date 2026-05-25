from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4", temperature=0.9, max_completion_tokens=2048)

result = model.invoke("What is the capital of France?")

print(result)