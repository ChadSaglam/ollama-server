from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI(title="Ollama ADHD Task API")

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.post("/analyze-task")
async def analyze_task(title: str, description: str):
    prompt = f"""
    [INST] Task Analysis Request:
    Title: {title}
    Description: {description}
    
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
                "model": "mistral",
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