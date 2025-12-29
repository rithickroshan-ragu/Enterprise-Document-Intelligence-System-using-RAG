from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import ask_llm

app = FastAPI()

# Allow local UI dev server to call the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Homepage from start_api"}


class ChatRequest(BaseModel):
    question: str


@app.post("/api/chat")
def chat(req: ChatRequest):
    # Dummy response for the UI to consume. Replace with real RAG logic.
    response = ask_llm(req.question)
    return {"reply": f"{response}"}
