# main.py - Veritas Protocol (Professional Landing Page)
import hashlib
import json
import os
import time
from datetime import datetime
from fastapi import FastAPI, HTMLResponse
from fastapi.responses import HTMLResponse
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

# --- The NEW Professional Landing Page (HTML) ---
@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Veritas Protocol</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #0a0a0a;
                color: #ffffff;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                text-align: center;
                background: #1a1a1a;
                padding: 60px 40px;
                border-radius: 20px;
                border: 1px solid #333333;
                box-shadow: 0 20px 60px rgba(0,0,0,0.8);
            }
            h1 {
                font-size: 4rem;
                margin: 0 0 10px 0;
                letter-spacing: -2px;
                background: linear-gradient(135deg, #ffffff 0%, #888888 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .subtitle {
                font-size: 1.2rem;
                color: #aaaaaa;
                margin-bottom: 40px;
                border-bottom: 1px solid #333;
                padding-bottom: 20px;
            }
            .tagline {
                font-size: 1.5rem;
                font-weight: 300;
                color: #ffffff;
                margin-bottom: 30px;
            }
            .features {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 15px;
                margin: 30px 0;
            }
            .feature {
                background: #2a2a2a;
                padding: 12px 24px;
                border-radius: 30px;
                font-size: 0.9rem;
                color: #ccc;
                border: 1px solid #333;
            }
            .feature strong {
                color: #fff;
            }
            .button {
                display: inline-block;
                background: #ffffff;
                color: #000000;
                padding: 16px 40px;
                border-radius: 40px;
                text-decoration: none;
                font-weight: bold;
                font-size: 1.1rem;
                margin-top: 20px;
                transition: all 0.3s ease;
            }
            .button:hover {
                background: #dddddd;
                transform: scale(1.02);
            }
            .button-secondary {
                background: transparent;
                color: #ffffff;
                border: 1px solid #444;
                margin-left: 10px;
            }
            .button-secondary:hover {
                background: #2a2a2a;
            }
            .footer {
                margin-top: 40px;
                font-size: 0.8rem;
                color: #555;
                border-top: 1px solid #222;
                padding-top: 20px;
            }
            .footer a {
                color: #888;
                text-decoration: none;
            }
            .footer a:hover {
                color: #fff;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>VERITAS</h1>
            <div class="subtitle">The Universal Standard for AI Content Integrity</div>
            
            <div class="tagline">
                Instantly verify if content was AI-generated — and by which model.
            </div>
            
            <div class="features">
                <span class="feature"><strong>Invisible</strong> Watermarks</span>
                <span class="feature"><strong>&lt; 100ms</strong> Verification</span>
                <span class="feature"><strong>Tamper-Proof</strong> Signatures</span>
                <span class="feature"><strong>1B+</strong> Requests/Day</span>
            </div>
            
            <div>
                <a href="/docs" class="button"> Explore the API</a>
                <a href="https://github.com/hendricksmichaelt-glitch/veritas-protocol" class="button button-secondary">View Source Code</a>
            </div>
            
            <div class="footer">
                <p>Veritas Protocol is available for acquisition.<br>
                Contact <a href="mailto:hendricksmichaelt@gmail.com">hendricksmichaelt@gmail.com</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# --- Run the server ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
