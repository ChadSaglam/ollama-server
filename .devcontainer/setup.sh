#!/bin/bash

set -e

# Start Ollama in background
echo "Starting Ollama..."
ollama serve &

# Wait for Ollama to initialize
sleep 5

# Pull model (optional)
ollama pull qwen2.5:3b || echo "Model already exists"

# Start FastAPI server
echo "Starting FastAPI server..."
uvicorn api.server:app --host 0.0.0.0 --port 8000