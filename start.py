from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import ask_llm, uplaod_documents, clear_database

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


# Endpoint: upload a PDF and save it locally (temporary storage)
import uuid
from pathlib import Path

UPLOAD_DIR = Path("tmp_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/api/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not (file.filename.lower().endswith(".pdf") or file.content_type == "application/pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    filename = f"{file.filename}_{uuid.uuid4().hex}"
    file_path = UPLOAD_DIR / filename
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        uplaod_documents(str(file_path))
    finally:
        await file.close()
    return {"filename": filename, "path": str(file_path)}



@app.post("/api/clear_session")
def clear_session():
    """Clear temporary uploads for the current server session.

    Deletes files and directories under `tmp_uploads/` and returns a list of removed items.
    """
    import shutil

    removed = []
    try:
        # 1. Delet uploaded PDF files 
        for child in UPLOAD_DIR.glob("*"):
            try:
                if child.is_file():
                    child.unlink()
                    removed.append(child.name)
                elif child.is_dir():
                    shutil.rmtree(child)
                    removed.append(child.name)
            except Exception:
                # skip items that can't be removed
                continue

        # 2. Clear chroma db data
        clear_database()
    except Exception:
        pass

    return {"status": "ok", "removed": removed}
