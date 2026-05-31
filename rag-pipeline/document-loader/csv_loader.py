from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path="./data/sample.csv")

documents = loader.lazy_load()

print(documents[0])

# you can use load only instead of lazy_load, but it will load all the documents into memory at once