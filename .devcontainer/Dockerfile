FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

RUN apt-get update && \
    apt-get install -y \
    curl \
    python3-pip \
    screen \ 
    && rm -rf /var/lib/apt/lists/*

# Ollama setup
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /workspace

# Python dependencies
RUN pip install fastapi uvicorn requests

# Model download (quantized version)
RUN ollama pull mistral:7b-instruct-q4_K_M &

COPY api /workspace/api
COPY .devcontainer/setup.sh /tmp/setup.sh
RUN chmod +x /tmp/setup.sh

CMD ["/tmp/setup.sh"]