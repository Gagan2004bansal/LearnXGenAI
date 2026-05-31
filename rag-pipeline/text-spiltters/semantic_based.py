from langchain.text_splitters import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

text_splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type="deviation",
    breakpoint_threshold_amount=1,
)

text = """This is a long text that needs to be split into smaller chunks.
The length of each chunk should not exceed a certain limit.
This is important for processing large documents and ensuring
that the text can be easily handled by various applications.

The SemanticChunker uses semantic similarity to split the text into chunks.
It can be useful for splitting text based on meaning rather than just length or structure.
"""

docs = text_splitter.create_documents([text])
print(len(docs))
print(docs)