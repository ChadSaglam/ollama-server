from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json

app = FastAPI(title="Ollama ADHD Task API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"

# Request modeli tanımla
class TaskRequest(BaseModel):
    title: str
    description: str

class PromptRequest(BaseModel):
    prompt: str
    model: str = "qwen2.5:3b"
    stream: bool = False

async def generate_text(request: PromptRequest = Body(...)):
    """
    General-purpose endpoint for sending prompts to Ollama models.
    Returns raw response from the model.
    """
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": request.model,
                "prompt": request.prompt,
                "stream": request.stream
            },
            timeout=60
        )

        if not response.ok:
            raise HTTPException(status_code=500, detail=f"Ollama error: {response.text}")

        data = response.json()

        return {
            "response": data.get("response", ""),
            "model": data.get("model", "")
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")
    
@app.post("/analyze-task")
async def analyze_task(request: TaskRequest = Body(...)):
    prompt = f"""
    [INST] Task Analysis Request:
    Title: {request.title}
    Description: {request.description}

    Please return JSON with:
    - priority (low/medium/high)
    - energyLevel (low/medium/high)
    - estimatedTimeMinutes (integer)
    - subtasks (array of strings)

    Example format:
    {{
      "priority": "high",
      "energyLevel": "medium",
      "estimatedTimeMinutes": 25,
      "subtasks": ["...", "..."]
    }}
    [/INST]
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": request.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        data = response.json()

        try:
            parsed = json.loads(data["response"])
            return parsed
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Model returned invalid JSON: {data['response']}")

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ollama API error: {str(e)}")
    
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "mistral:7b-instruct"}