from langchain_huggingface import ChathuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser, ResponseSchema

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
)

model = ChathuggingFace(llm=llm)

schema = [
    ResponseSchema(name='fact_1', description='Fact 1 about the topic'),
    ResponseSchema(name='fact_2', description='Fact 2 about the topic'),
    ResponseSchema(name='fact_3', description='Fact 3 about the topic'),
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template='Give 3 facts about the topic of {topic} \n {format_instructions}',
    input_variables=['topic'],
    partial_variables={
        'format_instructions': parser.get_format_instructions()
    }
)

prompt = template.invoke({'topic': 'black hole'})

result = model.invoke(prompt)
final = parser.parse(result.content)
print(final)