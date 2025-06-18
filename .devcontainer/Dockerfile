FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set up Python environment
WORKDIR /workspace

# Install Python packages (don't copy files yet)
RUN pip install fastapi uvicorn requests

# Copy setup script
COPY setup.sh /tmp/setup.sh
RUN chmod +x /tmp/setup.sh

# Expose ports
EXPOSE 11434 8000

# The files will be mounted by Codespaces, not copied
CMD ["/tmp/setup.sh"]