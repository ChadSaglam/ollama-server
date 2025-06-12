FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh  | sh

# Set up Python environment
WORKDIR /workspace
COPY api /workspace/api
RUN pip install fastapi uvicorn requests

# Copy setup script
COPY .devcontainer/setup.sh /tmp/setup.sh
RUN chmod +x /tmp/setup.sh

# Expose ports
EXPOSE 11434 8000

# Run everything
CMD ["/tmp/setup.sh"]