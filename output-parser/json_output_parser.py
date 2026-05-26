from langchain_huggingface import ChathuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
)

model = ChathuggingFace(llm=llm)

parser = JsonOutputParser()

template = PromptTemplate(
    template='Give me the name, age and city of a fictional person \n {format_instructions}',
    input_variables=[],
    partial_variables={
        'format_instructions': parser.get_format_instructions()
    }
)

prompt = template.format()

result = model.invoke(prompt)
final = parser.parse(result.content)
print(final)