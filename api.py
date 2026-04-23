from fastapi import FastAPI
from engine import process_query

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

app = FastAPI()


# ---------- Load once at startup ----------

embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

retriever = vector_db.as_retriever(search_kwargs={"k":5})

llm = Ollama(model="mistral")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

memory = {}


# ---------- API route ----------

@app.post("/chat")
def chat(query: str):

    embedding_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vector_db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model
    )

    retriever = vector_db.as_retriever(search_kwargs={"k":5})

    llm = Ollama(model="mistral")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    response = process_query(
        query,
        memory,
        qa_chain
    )

    return {"response": response}
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)