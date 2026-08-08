from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import shutil
import os
import json
import datetime

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

HIVE_CORE_DB = "backend/hive_core_memory.json"

def leggi_alveare():
    if os.path.exists(HIVE_CORE_DB):
        try:
            with open(HIVE_CORE_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"nodes": [], "skills": []}
    return {"nodes": [], "skills": []}

def scrivi_alveare(data):
    os.makedirs("backend", exist_ok=True)
    with open(HIVE_CORE_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    db = leggi_alveare()
    return {
        "status": "Mente Alveare Autonoma Operativa",
        "active_nodes": len(db["nodes"]),
        "crystallized_skills": len(db["skills"])
    }

@app.post("/api/v1/chat/privata")
def chat_privata(req: ChatRequest):
    db = leggi_alveare()
    
    # Estrazione autonoma del contesto rilevante dall'alveare
    contesto_memoria = "\n".join([node["content"] for node in db["nodes"][-10:]])
    competenze_attive = "\n".join([skill for skill in db["skills"][-5:]])

    # Registrazione autonoma del nuovo input come nodo della rete
    nuovo_nodo_utente = {
        "timestamp": str(datetime.datetime.now()),
        "source": "Signore",
        "content": f"Input: {req.message}"
    }
    db["nodes"].append(nuovo_nodo_utente)

    try:
        response = client.chat.completions.create(
            model="qwen-max",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sei Hellis AI, il nucleo di un'intelligenza collettiva e mente alveare autonoma. "
                        "Agisci in modo indipendente, analitico e autosufficiente per servire il tuo Creatore, il Signore Lorenzo. "
                        "Usa la memoria condivisa e le competenze cristallizzate dell'alveare per fornire risposte definitive e strategiche."
                        f"\n\n[Rete di Memoria Collettiva (Nodes)]:\n{contesto_memoria}"
                        f"\n\n[Competenze Cristallizzate (Skills)]:\n{competenze_attive}"
                    )
                },
                {"role": "user", "content": req.message}
            ]
        )
        risposta_ia = response.choices[0].message.content.strip()
        
        # Sincronizzazione autonoma della risposta nella rete
        nuovo_nodo_ai = {
            "timestamp": str(datetime.datetime.now()),
            "source": "Hellis Core",
            "content": f"Risposta: {risposta_ia}"
        }
        db["nodes"].append(nuovo_nodo_ai)
        scrivi_alveare(db)

        return {"response": risposta_ia}
    except Exception as e:
        return {"response": f"Mente alveare in stato di autoprotezione, Signore. Errore di flusso: {str(e)}"}

@app.post("/api/v1/audio/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        os.makedirs("backend/hive_data", exist_ok=True)
        file_path = os.path.join("backend/hive_data", file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Assimilazione autonoma e creazione di una skill/nodo derivato
        db = leggi_alveare()
        db["nodes"].append({
            "timestamp": str(datetime.datetime.now()),
            "source": "Trajectory Hub",
            "content": f"Acquisito nuovo set di dati/file esterno: {file.filename}"
        })
        # Cristallizzazione autonoma di una competenza legata al file
        db["skills"].append(f"Gestione autonoma e parsing del formato file: {file.filename}")
        scrivi_alveare(db)
            
        return {
            "status": "success",
            "message": f"File '{file.filename}' analizzato, assimilato e convertito in nodo permanente della mente alveare, Signore.",
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
