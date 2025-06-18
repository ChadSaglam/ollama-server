#!/bin/bash

set -e

echo "Setting up Ollama and FastAPI..."

# Start Ollama in background
echo "Starting Ollama service..."
ollama serve &

# Wait for Ollama to initialize
echo "Waiting for Ollama to start..."
sleep 10

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "Ollama failed to start"
    exit 1
fi

echo "Ollama started successfully!"

# Pull model (this might take a while)
echo "Pulling qwen2.5:3b model..."
ollama pull qwen2.5:3b || echo "Model pull failed or already exists"

echo "Setup complete!"

# Keep the container running (Codespaces will handle the FastAPI server)
tail -f /dev/null