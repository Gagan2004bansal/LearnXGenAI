from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI()

Prompt = PromptTemplate(
    template="What is the content of the following text file? {file_content}",
    input_variables=["file_content"],
)

parser = StrOutputParser()

loader = TextLoader("path_to_file.txt", encoding="utf-8")

docs = loader.load()

chain = prompt | model | parser

res = chain.invoke({'file_content':docs[0].page_content})

print(res)