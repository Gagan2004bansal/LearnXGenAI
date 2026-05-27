from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel

load_dotenv()

model1 = ChatOpenAI()
model2 = ChatOpenAI()

prompt1 = PromptTemplate(
    template='Generate short and simple notes from the following text \n {text}',
    input_variables=['text'],
)

prompt2 = PromptTemplate(
    template='Generate a 5 short Q/A pairs from the following text \n {text}',
    input_variables=['text'],
)

prompt3 = PromptTemplate(
    template='Merge the following notes and Q/A pairs into a single document \n Notes: {notes} \n Q/A pairs: {qa_pairs}',
    input_variables=['notes', 'quiz'],
)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    'notes': prompt1 | model1 | parser,
    'quiz': prompt2 | model2 | parser,
})

merge_chain = prompt3 | model1 | parser

chain = parallel_chain | merge_chain

text = """Machine learning workflows are often composed of different parts. A typical pipeline consists of a pre-processing step that transforms or imputes the data, and a final predictor that predicts target values.

In scikit-learn, pre-processors and transformers follow the same API as the estimator objects (they actually all inherit from the same BaseEstimator class). The transformer objects don’t have a predict method but rather a transform method that outputs a newly transformed sample matrix X"""

response = chain.invoke({'text': text})

chain.get_graph().print_ascii()
