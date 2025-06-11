# Start ollama service
ollama serve > /tmp/ollama.log 2>&1 &

uvicorn api.server:app --host 0.0.0.0 --port 8000