from langchain_huggingface import ChathuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
)

model = ChathuggingFace(llm=llm)

class Person(BaseModel):
    name: str = Field(description='The name of the person')
    age: int = Field(gt=18, description='The age of the person')
    city: str = Field(description='The city where the person lives')


parser = PydanticOutputParse(pydantic_model=Person)

template = PromptTemplate(
    template='Generate me the name, age and city of a fictional {place} person \n {format_instructions}',
    input_variables=['place'],
    partial_variables={
        'format_instructions': parser.get_format_instructions()
    }
)

prompt = template.format()

result = model.invoke(prompt)
final = parser.parse(result.content)
print(final)