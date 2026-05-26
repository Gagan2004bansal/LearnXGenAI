from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated

load_dotenv()

model = ChatOpenAI()

# schema 
json_schema = {
    "summary": {
        "type": "string",
        "description": "A brief summary of the review"
    }
    "sentiment": {
        "type": "string",
        "description": "The overall sentiment of the review (positive, negative, neutral)"
    }
}

structured_model = model.with_structured_output(json_schema)

result = structured_model.invoke("""The hardware is great, but the software feels bloated. There are too
many pre-installed apps that I can't remove. Also, the UI looks outdated compared to other
brands. Hoping for a software update to improve the user experience.""")

print(result) 