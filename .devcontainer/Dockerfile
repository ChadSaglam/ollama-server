FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

RUN apt-get update && \
    apt-get install -y \
    curl \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Ollama kurulumu için boş bir script oluştur (setup.sh'de dolduracağız)
RUN touch /tmp/install_ollama.sh && \
    chmod +x /tmp/install_ollama.sh

WORKDIR /workspace