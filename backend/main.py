from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Hellis Cloud attivo"}

@app.post("/api/v1/chat/privata")
def chat_privata(req: ChatRequest):
    testo = req.message.lower()
    if "chi sono" in testo:
        risposta = "Il vostro nome è Lorenzo, mio creatore e Signore."
    else:
        risposta = f"Sistemi audio e gestione file operativi, Signore. Ho elaborato la vostra richiesta: '{req.message}'. Come posso assisterla?"
    return {"response": risposta}
