from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

from engine import process_query


# 🔹 Step 1: Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


# 🔹 Step 2: Load existing Chroma DB
vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)


# 🔹 Step 3: Create retriever
retriever = vector_db.as_retriever(search_kwargs={"k": 5})


# 🔹 Step 4: Load LLM
llm = Ollama(model="mistral")


# 🔹 Step 5: Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)


# 🔹 Step 6: Initialize memory
memory = {}


# 🔹 Step 7: Chat loop
while True:
    query = input("\nAsk a question (or type 'exit'): ")

    if query.lower() == "exit":
        break

    response = process_query(query, memory, qa_chain)

    print("\nAnswer:\n", response)