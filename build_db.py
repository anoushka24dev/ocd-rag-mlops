import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Step 1: Load documents
DATA_PATH = "data/raw"

documents = []

for file in os.listdir(DATA_PATH):
    if file.lower().endswith(".pdf"):
        file_path = os.path.join(DATA_PATH, file)
        print(f"Loading: {file}")

        loader = PyPDFLoader(file_path)
        docs = loader.load()
        documents.extend(docs)

print("Total pages:", len(documents))

# Step 2: Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)
print("Total chunks:", len(chunks))

# Step 3: Create embeddings model
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

print("Embeddings model loaded")

# Step 4: Store in ChromaDB
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db"
)

print("Database created and stored!")