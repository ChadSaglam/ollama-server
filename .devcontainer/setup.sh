# Ollama setup
curl -fsSL https://ollama.com/install.sh | sh

# Python dependencies
pip install fastapi uvicorn requests

# Model download (quantized version)
ollama pull mistral:7b-instruct-q4_K_M &

# Start FastAPI server in background
nohup uvicorn api.server:app --host 0.0.0.0 --port 8000 > /tmp/fastapi.log 2>&1 &

# Start ollama service
nohup ollama serve > /tmp/ollama.log 2>&1 &