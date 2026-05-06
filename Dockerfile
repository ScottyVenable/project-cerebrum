# Use a lightweight Debian-based Python image for ARM compatibility
FROM python:3.11-slim-bookworm

# Install system dependencies for LSL and signal processing
RUN apt-get update && apt-get install -y \
    liblsl-dev \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY server/ ./server/
COPY ai_models/ ./ai_models/

# Default command: Launch the Processing Hub
CMD ["python", "server/hub.py"]
