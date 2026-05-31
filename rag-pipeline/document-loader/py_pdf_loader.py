from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("path_to_file.pdf")

docs = loader.load()

print(len(docs))