from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableBranch, RunnableLambda
from langchain_core.output_parser import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import literal

load_dotenv()

model = ChatOpenAI()
parser = StrOutputParser()

class Feedback(BaseModel):
    sentiment: literal['positive', 'negative'] = Field(description='Give the sentiment of the feedback text')

parser2 = PydanticOutputParser(pydantic_object=Feedback)

prompt1 = PromptTemplate(
    template='Classify the sentiment of the following feedback text as positive or negative \n {feedback} \n {format_instructions}',
    input_variables=['feedback'],
    partial_variables={'format_instructions': parser2.get_format_instructions()},
)

classfier_chain = prompt1 | model | parser2

prompt2 = PromptTemplate(
    template='Write an appropriate response to this positive feedback \n {feedback}',
    input_variables=['feedback'],
)

prompt3 = PromptTemplate(
    template='Write an appropriate response to this negative feedback \n {feedback}',
    input_variables=['feedback'],
)

branch_chain = RunnableBranch(
    (lambda x: x.sentiment == 'positive',  prompt2 | model | parser),
    (lambda x: x.sentiment == 'negative',  prompt3 | model | parser),
    RunnableLambda(lambda x: "Could not find sentiment")
)

chain = classfier_chain | branch_chain

feedback = "I love this product! It has changed my life for the better."
response = chain.invoke({'feedback': feedback})
print(response)
