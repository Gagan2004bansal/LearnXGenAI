from langchain.text_splitters import BaseTextSplitter

text = """This is a long text that needs to be split into smaller chunks.
 The length of each chunk should not exceed a certain limit.
  This is important for processing large documents and ensuring
   that the text can be easily handled by various applications."""

splitter = CharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10,
    separator="",
)

split_text = splitter.split_text(text)