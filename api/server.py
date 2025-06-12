from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests
import json
import time

app = FastAPI(title="Ollama API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"

class TaskRequest(BaseModel):
    title: str
    description: str
    model: Optional[str] = "qwen2.5:3b"

class PromptRequest(BaseModel):
    prompt: str
    model: str = "qwen2.5:3b"
    stream: bool = False

@app.post("/generate")
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
    You are an AI assistant helping someone with ADHD organize tasks efficiently.
 
    Return ONLY a valid JSON object with:
    - priority (low/medium/high)
    - energyLevel (low/medium/high)
    - estimatedTimeMinutes (integer)
    - subtasks (array of strings)
 
    DO NOT include any markdown formatting, explanations, or extra text before or after the JSON.
 
    Your task breakdown should be as detailed as possible. Aim for at least 5–7 clear, actionable subtasks.
 
    Example format:
    {{
        "priority": "medium",
        "energyLevel": "medium",
        "estimatedTimeMinutes": 45,
        "subtasks": [
            "Subtask 1 description",
            "Subtask 2 description",
            "Subtask 3 description",
            "Subtask 4 description",
            "Subtask 5 description"
        ]
    }}
 
    Now analyze this task:
    Title: {request.title}
    Description: {request.description}
 
    JSON output:
    """
 
    start_time = time.time()
 
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": request.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        inference_time = time.time() - start_time
 
        data = response.json()
 
        try:
            parsed = json.loads(data["response"])
            return {
                "inference_time_seconds": round(inference_time, 2),
                "result": parsed
            }
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Model returned invalid JSON: {data['response']}")
 
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ollama API error: {str(e)}")
 
@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "qwen2.5:3b"}

@app.get("/model-ready")
async def model_ready():
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": "Test",
                "stream": False
            },
            timeout=5
        )
        return {"ready": True}
    except (requests.ConnectionError, requests.Timeout, requests.RequestException):
        return {"ready": False}
