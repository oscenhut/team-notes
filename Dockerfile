# Base image: Python 3.13 slim for lightweight production footprint
FROM python:3.13-slim

# Prevent Python from writing .pyc files and enable unbuffered output for clean logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install essential build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory for persistent SQLite storage
RUN mkdir -p /app/data

# Copy application source code
COPY . .

# Expose default FastAPI / Uvicorn port
EXPOSE 8000

# Production Uvicorn command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]