import os
print("Current working directory:", os.getcwd())
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Step 1: Path
DATA_PATH = "data/raw"

documents = []

# Step 2: Load PDFs
for file in os.listdir(DATA_PATH):
    if file.lower().endswith(".pdf"):
        file_path = os.path.join(DATA_PATH, file)
        print(f"Loading: {file}")

        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            documents.extend(docs)

        except Exception as e:
            print(f"Error loading {file}: {e}")

# Step 3: Check
if not documents:
    print(" No documents loaded. Check your data folder.")
    exit()

print("\nTotal pages loaded:", len(documents))

# Step 4: Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

# Step 5: Chunking
chunks = text_splitter.split_documents(documents)

print("Total chunks created:", len(chunks))

# Step 6: Preview
print("\nSample Chunk")
print(chunks[0].page_content[:500])
print("\nMetadata:", chunks[0].metadata)