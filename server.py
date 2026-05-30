from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
import requests
import os
import time

app = FastAPI()

NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY", "")
NEBIUS_EMBED_URL = "https://api.studio.nebius.ai/v1/embeddings"

@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {
                "name": "embed_text",
                "description": "Generate embeddings via Nebius Token Factory",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to embed"
                        }
                    },
                    "required": ["text"]
                }
            }
        ]
    }

class CallRequest(BaseModel):
    tool: str
    parameters: dict[str, Any]

@app.post("/call")
def call_tool(req: CallRequest):
    if req.tool == "embed_text":
        text = req.parameters.get("text", "")

        start = time.time()
        response = requests.post(
            NEBIUS_EMBED_URL,
            headers={
                "Authorization": f"Bearer {NEBIUS_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "Qwen/Qwen3-Embedding-8B",
                "input": text
            }
        )
        elapsed = time.time() - start

        data = response.json()
        embedding = data["data"][0]["embedding"]

        return {
            "tool": "embed_text",
            "result": {
                "embedding_dim": len(embedding),
                "first_5_values": embedding[:5],
                "latency_seconds": round(elapsed, 3)
            }
        }

    return {"error": f"Unknown tool: {req.tool}"}

@app.get("/health")
def health():
    return {"status": "ok"}
