from langchain.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader

loader = DirectoryLoader(
    path="./data",
    glob='**/*.{pdf}',
    loader_cls=PyPDFLoader
)

docs = loader.load()
print(len(docs))