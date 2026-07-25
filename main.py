# main.py - Veritas Protocol
import hashlib
import json
import os
import time
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# --- Initialize the app ---
app = FastAPI(title="Veritas Protocol", version="1.0")

# --- The "Ledger" (Simple database) ---
LEDGER_FILE = "ledger.json"

def load_ledger():
    if not os.path.exists(LEDGER_FILE):
        return []
    with open(LEDGER_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_to_ledger(record):
    ledger = load_ledger()
    ledger.append(record)
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=2)

# --- The "Watermark" Engine ---
def generate_signature(owner_id: str, model_name: str = "unknown") -> dict:
    timestamp = datetime.now().isoformat()
    unique_string = f"{owner_id}:{model_name}:{timestamp}:{time.time()}"
    signature = hashlib.sha256(unique_string.encode()).hexdigest()
    
    return {
        "signature": signature,
        "timestamp": timestamp,
        "owner_id": owner_id,
        "model_name": model_name,
        "verified": True
    }

# --- The API Endpoints ---
class WatermarkRequest(BaseModel):
    owner_id: str
    model_name: str = "unknown"

class VerifyRequest(BaseModel):
    signature: str

@app.post("/watermark")
async def embed_watermark(request: WatermarkRequest):
    signature_data = generate_signature(request.owner_id, request.model_name)
    save_to_ledger(signature_data)
    return {
        "status": "success",
        "data": signature_data
    }

@app.post("/verify")
async def verify_watermark(request: VerifyRequest):
    ledger = load_ledger()
    for record in ledger:
        if record["signature"] == request.signature:
            return {
                "verified": True,
                "data": record
            }
    return {
        "verified": False,
        "message": "Signature not found."
    }

@app.get("/")
async def root():
    return {
        "message": "Veritas Protocol: The Universal Standard for AI Content Integrity",
        "endpoints": {
            "/watermark (POST)": "Create a watermark",
            "/verify (POST)": "Verify a watermark"
        }
    }

# --- Run the server ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)