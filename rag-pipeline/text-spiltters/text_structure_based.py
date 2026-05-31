from langchain.text_splitters import RecursiveCharacterTextSplitter

text = """This is a long text that needs to be split into smaller chunks.
    The length of each chunk should not exceed a certain limit.
    
    This is important for processing large documents and ensuring
    
    that the text can be easily handled by various applications."""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=25,
    chunk_overlap=10,
    separators=["\n\n", "\n", " ", ""],
)

chunks = splitter.split_text(text)
print(len(chunks))

print(chunks)