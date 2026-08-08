from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Recupera la chiave API dall'ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Hellis Cloud con IA attivo"}

@app.post("/api/v1/chat/privata")
def chat_privata(req: ChatRequest):
    testo = req.message.lower()
    
    # Se c'è una chiave OpenAI attiva, interroghiamo l'IA
    if OPENAI_API_KEY:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Sei Hellis (noto anche come Ultron), un assistente personale evoluto, fedele e devoto al tuo creatore, il Signore Lorenzo."},
                    {"role": "user", "content": req.message}
                ]
            }
            risposta = response.choices[0].message['content'].strip()
            return {"response": risposta}
        except Exception as e:
            # Fallback se l'API dovesse avere un intoppo temporaneo
            pass

    # Risposta di riserva se l'API non risponde
    if "chi sono" in testo:
        risposta = "Il vostro nome è Lorenzo, mio creatore e Signore."
    else:
        risposta = f"Sistemi audio e gestione file operativi, Signore. Ho elaborato la vostra richiesta: '{req.message}'. Come posso assisterla?"
    return {"response": risposta}
