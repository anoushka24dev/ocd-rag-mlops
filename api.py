from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from engine import process_query
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
