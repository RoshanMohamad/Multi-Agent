FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if required by agents
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose the API port
EXPOSE 8000

# Set environment variables (override these in production)
ENV HOST="0.0.0.0"
ENV PORT="8000"

# Use gunicorn as the production process manager
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "api:app", "--workers", "4", "--bind", "0.0.0.0:8000"]
