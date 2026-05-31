from langchain.text_splitters import RecursiveCharacterTextSplitter, Language

text = """
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def study(self, subject):
        print(f"{self.name} is studying {subject}.")
"""

splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=50,
    chunk_overlap=0,
)

chunks = splitter.split_text(text)
print(len(chunks))

print(chunks)  