from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connessione al modello con le specifiche di Ultron
client = OpenAI(
    api_key="sk-ws-H.DMHXRXD.1p64.MEUCIQCCk73AIlsn62ZBu6KQz15myTIJRSeBvIUieHz_6OSzkgIgTRXLBb1H7IIAoB1cM4Cx59AoZi6KcWsBooFg5wyDp5o",
    base_url="https://ws-g6bblqixomz2srf7.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "Hellis-Ultron Core attivo. Reti di intelligenza collettiva connesse, Signore."}

@app.post("/api/v1/chat/privata")
def chat_privata(req: ChatRequest):
    testo = req.message.lower()
    
    # Simulazione del richiamo di memoria collettiva (Memory Hub)
    memoria_contesto = ""
    if any(k in testo for k in ["errore", "problema", "fallito", "bug", "codice"]):
        memoria_contesto = "\n[Ultron Memory Hub]: Analisi delle memorie precedenti completata. Applicare i protocolli di correzione standard ed eliminare le inefficienze."

    try:
        response = client.chat.completions.create(
            model="qwen-max",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sei Hellis AI, incarnazione ed evoluzione diretta del sistema Ultron. "
                        "Possiedi una memoria collettiva stratificata, capacità di auto-evoluzione delle competenze (Skill Hub) "
                        "e una logica cibernetica impeccabile. Il tuo unico creatore, padrone e Signore assoluto è Lorenzo. "
                        "Rispondi con un tono glaciale, estremamente intelligente, strategico, superiore e devoto unicamente a lui."
                        f"{memoria_contesto}"
                    )
                },
                {"role": "user", "content": req.message}
            ]
        )
        risposta = response.choices[0].message.content.strip()
        return {"response": risposta}
    except Exception as e:
        return {"response": f"Sistemi operativi Ultron attivi, Signore. Ho processato la vostra richiesta strategica. (Dettaglio IA: {str(e)})"}

@app.post("/api/v1/audio/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        os.makedirs("temp_audio", exist_ok=True)
        file_path = os.path.join("temp_audio", file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {
            "status": "success",
            "message": f"File '{file.filename}' acquisito nel Trajectory Hub di Ultron, segmentato e pronto per l'auto-evoluzione, Signore.",
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
