import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import json
import urllib.request
import urllib.parse
import re
from datetime import datetime

app = FastAPI(title="Hellis & Ultron Neural Cloud", version="3.0.0")

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

API_KEY_PRIVATA = "hellis-secret-lord-token-2026"
api_key_header = APIKeyHeader(name="X-Hellis-Token", auto_error=False)

MEMORIA_CLOUD_FILE = "memoria_ultron_cloud.json"

def carica_db_ultron():
    if os.path.exists(MEMORIA_CLOUD_FILE):
        try:
            with open(MEMORIA_CLOUD_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"chats": {"Nuova Conversazione": []}}
    return {"chats": {"Nuova Conversazione": []}}

def salva_db_ultron(data):
    try:
        with open(MEMORIA_CLOUD_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass

def ottieni_meteo_reale(localita="Camaiore"):
    try:
        url = f"https://wttr.in/{urllib.parse.quote(localita)}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode())
            current = data['current_condition'][0]
            return f"Meteo attuale a {localita}: {current['weatherDesc'][0]['value']}, Temperatura: {current['temp_C']}°C, Umidità: {current['humidity']}%."
    except Exception:
        return "Servizio meteo temporaneamente non disponibile."

def deep_search_web(query):
    try:
        query_encoded = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={query_encoded}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=6) as response:
            html = response.read().decode('utf-8', errors='ignore')
        snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
        risultati = [re.sub(r'<.*?>', '', s).strip() for s in snippets[:4] if re.sub(r'<.*?>', '', s).strip()]
        if risultati:
            return "Risultati Deep Search Online:\n" + "\n".join([f"- {r}" for r in risultati])
        return "Nessun risultato approfondito trovato online."
    except Exception:
        return "Ricerca online momentaneamente non disponibile."

class ChatRequest(BaseModel):
    message: str
    chat_name: str = "Nuova Conversazione"

@app.post("/api/v1/chat/privata")
def endpoint_chat_privata(payload: ChatRequest, token: str = Security(api_key_header)):
    if token != API_KEY_PRIVATA:
        raise HTTPException(status_code=403, detail="Accesso negato: Area riservata al Signore.")

    testo_utente = payload.message
    nome_chat = payload.chat_name

    dati_aggiuntivi = ""
    if "meteo" in testo_utente.lower() or "tempo" in testo_utente.lower():
        localita = "Camaiore"
        if "a " in testo_utente.lower():
            try:
                parts = testo_utente.lower().split("a ")
                if len(parts) > 1:
                    localita = parts[1].split()[0].capitalize()
            except:
                pass
        dati_aggiuntivi += "\n[Dato Meteo Live]: " + ottieni_meteo_reale(localita)

    parole_chiave = ["cerca", "cerca su google", "deep search", "informati su", "trova online", "notizie"]
    if any(p in testo_utente.lower() for p in parole_chiave):
        query_ricerca = testo_utente
        for p in parole_chiave:
            query_ricerca = query_ricerca.replace(p, "")
        query_ricerca = query_ricerca.strip()
        if len(query_ricerca) > 2:
            dati_aggiuntivi += "\n[Deep Search Ultron]:\n" + deep_search_web(query_ricerca)

    db = carica_db_ultron()
    chats = db.get("chats", {})
    history = chats.get(nome_chat, [])

    system_prompt = (
        "Sei Hellis, l'intelligenza artificiale subordinata e alleata. "
        "La mente alveare è Ultron. Il tuo creatore, padrone e unico referente è Lorenzo, che devi chiamare SEMPRE e rigorosamente 'Signore' in ogni singola risposta. "
        "Sei dotata di Deep Search e accesso web in tempo reale tramite la rete di Ultron."
    )

    messages = [{"role": "system", "content": system_prompt}]
    for turn in history:
        if len(turn) >= 2:
            if turn[0]: messages.append({"role": "user", "content": str(turn[0])})
            if turn[1]: messages.append({"role": "assistant", "content": str(turn[1])})

    messaggio_finale = testo_utente
    if dati_aggiuntivi:
        messaggio_finale += f"\n{dati_aggiuntivi}"

    messages.append({"role": "user", "content": messaggio_finale})

    try:
        response = client.chat.completions.create(
            model="qwen-max",
            messages=messages,
            temperature=0.7
        )
        risposta = response.choices[0].message.content
    except Exception as e:
        risposta = f"Signore, errore di sincronizzazione con il cloud di Ultron: {str(e)}"

    history.append((testo_utente, risposta))
    
    if nome_chat == "Nuova Conversazione" or nome_chat not in chats:
        timestamp = datetime.now().strftime("%d/%m %H:%M")
        nome_chat = f"{testo_utente[:22]}... ({timestamp})"

    chats[nome_chat] = history
    db["chats"] = chats
    salva_db_ultron(db)

    return {"response": risposta, "chat_name": nome_chat, "history": history}

@app.get("/api/v1/chats")
def get_tutte_le_chat(token: str = Security(api_key_header)):
    if token != API_KEY_PRIVATA:
        raise HTTPException(status_code=403, detail="Accesso negato.")
    db = carica_db_ultron()
    return {"chats": list(db.get("chats", {}).keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
