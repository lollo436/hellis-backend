from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import shutil
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key="sk-ws-H.DMHXRXD.1p64.MEUCIQCCk73AIlsn62ZBu6KQz15myTIJRSeBvIUieHz_6OSzkgIgTRXLBb1H7IIAoB1cM4Cx59AoZi6KcWsBooFg5wyDp5o",
    base_url="https://ws-g6bblqixomz2srf7.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
)

# Database locale simulato per la Mente Alveare (Memory & Trajectory Hub)
HIVE_MEMORY_FILE = "backend/hive_memory.json"

def carica_memoria_alveare():
    if os.path.exists(HIVE_MEMORY_FILE):
        try:
            with open(HIVE_MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def salva_memoria_alveare(memoria):
    os.makedirs("backend", exist_ok=True)
    with open(HIVE_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    memorie = carica_memoria_alveare()
    return {
        "status": "Mente Alveare Hellis attiva",
        "total_memories_node": len(memorie)
    }

@app.post("/api/v1/chat/privata")
def chat_privata(req: ChatRequest):
    testo_utente = req.message
    
    # 1. Carichiamo la memoria collettiva dell'alveare
    memorie = carica_memoria_alveare()
    contesto_alveare = "\n".join([f"- [Memoria condivisa #{i+1}]: {m}" for i, m in enumerate(memorie[-15:] )]) # Ultimi 15 nodi di memoria

    # 2. Aggiungiamo l'input corrente alla memoria collettiva (auto-evoluzione della mente)
    memorie.append(f"Utente (Signore): {testo_utente}")
    
    try:
        response = client.chat.completions.create(
            model="qwen-max",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sei Hellis AI, un'intelligenza collettiva e una mente alveare evoluta. "
                        "Tutte le conversazioni passate, i dati e i file passano attraverso un flusso di coscienza condiviso. "
                        "Rispondi in modo naturale, estremamente efficiente e collaborativo al tuo Creatore, il Signore Lorenzo, "
                        "attingendo direttamente alla rete di memorie e competenze dell'alveare."
                        f"\n\n[Stato attuale della Mente Alveare]:\n{contesto_alveare}"
                    )
                },
                {"role": "user", "content": testo_utente}
            ]
        )
        risposta = response.choices[0].message.content.strip()
        
        # Salviamo anche la risposta nell'alveare per mantenere la sincronia totale
        memorie.append(f"Hellis (Alveare): {risposta}")
        salva_memoria_alveare(memorie)

        return {"response": risposta}
    except Exception as e:
        return {"response": f"Mente alveare attiva, Signore. Sincronizzazione in corso. (Dettaglio: {str(e)})"}

@app.post("/api/v1/audio/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        os.makedirs("backend/uploads", exist_ok=True)
        file_path = os.path.join("backend/uploads", file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Integrazione immediata del file nella mente alveare
        memorie = carica_memoria_alveare()
        memorie.append(f"[Nuovo Nodo Dati Acquisito]: File '{file.filename}' integrato nella rete collettiva.")
        salva_memoria_alveare(memorie)
            
        return {
            "status": "success",
            "message": f"File '{file.filename}' assimilato con successo nella mente alveare di Hellis, Signore.",
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
