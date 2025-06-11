from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

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
    - subtasks (array)
    [/INST]
    """
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "deepseek-r1:1.5b",
                "prompt": prompt,
                "format": "json",
                "stream": False
            },
            timeout=30
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "mistral:7b-instruct"}