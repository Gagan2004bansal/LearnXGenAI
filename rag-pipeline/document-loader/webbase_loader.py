from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI()

Prompt = PromptTemplate(
    template="What is the content of the following web page? {url}",
    input_variables=["url"],
)

parser = StrOutputParser()

url = "https://gagan-eosin.vercel.app/"
loader = WebBaseLoader(url)

docs = loader.load()

chain = prompt | model | parser

res = chain.invoke({'question': 'Name of the website owner', 'url':docs[0].page_content})

print(res)