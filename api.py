from fastapi import FastAPI
from engine import process_query
app = FastAPI()

# tiny in-memory conversation memory only
memory = {}

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "OCD bot API deployed successfully"
    }

@app.post("/chat")
def chat(query: str):

    # TEMPORARILY no LangChain / no Chroma / no Ollama
    # just use your engine logic only
    response = process_query(
        query,
        memory,
        None
    )

    return {
        "response": response
    }
