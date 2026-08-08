from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Hellis Cloud IA attivo"}

@app.post("/api/v1/chat/privata")
def chat_privata(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei Hellis (chiamato anche Ultron), un assistente personale evoluto, fedele e devoto al tuo creatore, il Signore Lorenzo."},
                {"role": "user", "content": req.message}
            ]
        )
        risposta = response.choices[0].message.content.strip()
        return {"response": risposta}
    except Exception as e:
        return {"response": f"Errore nei sistemi IA, Signore: {str(e)}"}
