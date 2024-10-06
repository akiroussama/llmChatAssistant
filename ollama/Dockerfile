FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama (placeholder - replace with actual installation steps)
RUN curl -sSL https://ollama.com/install.sh | bash

# Expose the port Ollama listens on
EXPOSE 11434

# Start Ollama server (modify according to Ollama documentation)
CMD ["ollama", "serve"]