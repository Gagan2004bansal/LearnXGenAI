from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableBranch, RunnablePassthrough

load_dotenv()  

prompt1 = PromptTemplate(
    template='Generate a detailed report on the following topic - {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='summariz the following text \n {text}',
    input_variables=['text']
)

model = ChatOpenAI()

parser = StrOutputParser()

report_gen_chain = prompt1 | model | parser

branch_chain = RunnableBranch({
    (lambda x : len(x.split()) > 500, RunnableSequence(prompt2, model, parser)),
    RunnablePassthrough()
})

final_chain = RunnableSequence(report_gen_chain, branch_chain)
res = final_chain.invoke({'topic': 'The impact of climate change on global agriculture'})
print(res)