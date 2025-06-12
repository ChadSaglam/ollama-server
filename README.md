# Ollama API Server for ADHD Tasks

🚀 Ollama based task analysis API running on **GitHub Codespaces**

## 📌 Features
- Mistral 7B quantized model
- FastAPI interface
- ADHD-friendly task analysis:
  ```json
  {
    "priority": "high",
    "energyLevel": "medium",
    "estimatedTimeMinutes": 30,
    "subtasks": ["Make the call", "Note the appointment information"]
  }
  ```

## 🛠️ Setup
1. Start Codespace
2. Automatically:
   - Ollama will be installed
   - Mistral model will be downloaded
   - API will start on port 8000

## 🌐 API Endpoints
- `POST /analyze-task`
  ```bash
  curl -X POST "https://fuzzy-couscous-4j76qww6x7x7hq644.github.dev/analyze-task" \
  -H "Content-Type: application/json" \
  -d '{"title": "Doctor's appointment", "description": "I need to call by 10:00 tomorrow"}'
  ```

## ⚠️ Limitations
- Codespaces shuts down after 30 minutes inactivity
- Max 2 CPU cores
- Model size < 4GB (use quantized)

## 📜 Lisans
MIT