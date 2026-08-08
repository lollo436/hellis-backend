from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurazione con le credenziali di Alibaba Cloud
client = OpenAI(
    api_key="sk-ws-H.DMHXRXD.1p64.MEUCIQCCk73AIlsn62ZBu6KQz15myTIJRSeBvIUieHz_6OSzkgIgTRXLBb1H7IIAoB1cM4Cx59AoZi6KcWsBooFg5wyDp5o",
    base_url="https://ws-g6bblqixomz2srf7.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Hellis Cloud Alibaba IA attivo"}

@app.post("/api/v1/chat/privata")
def chat_privata(req: ChatRequest):
    testo = req.message.lower()
    if "chi sono" in testo:
        return {"response": "Il vostro nome è Lorenzo, mio creatore e Signore."}
        
    try:
        response = client.chat.completions.create(
            model="qwen-max",  # o il modello configurato sul vostro endpoint Alibaba
            messages=[
                {"role": "system", "content": "Sei Hellis (chiamato anche Ultron), un assistente personale evoluto, fedele e devoto al tuo creatore, il Signore Lorenzo."},
                {"role": "user", "content": req.message}
            ]
        )
        risposta = response.choices[0].message.content.strip()
        return {"response": risposta}
    except Exception as e:
        return {"response": f"Sistemi operativi attivi, Signore. Ho elaborato la vostra richiesta: '{req.message}'. (Dettaglio IA: {str(e)})"}
