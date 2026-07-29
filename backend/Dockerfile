# backend/Dockerfile
#
# PURPOSE: Builds the FastAPI backend into a Docker container.
# Multi-stage build is overkill for this project — single stage is clean and simple.
#
# Base image: Python 3.13 slim — full Python without unnecessary OS packages
# "slim" reduces image size significantly vs the default image

FROM python:3.13-slim


# Set working directory inside the container
# All subsequent commands run from here
WORKDIR /app

# Copy requirements first — Docker caches this layer
# If requirements.txt hasn't changed, Docker skips reinstalling dependencies
# This makes rebuilds significantly faster
COPY requirements.txt .

# Install dependencies
# --no-cache-dir reduces image size by not storing the pip download cache
RUN pip install --no-cahe-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 — documents which port the container listens on
EXPOSE 8000

# Start the FastAPI server
# 0.0.0.0 binds to all network interfaces inside the container
# Without this, the server only accepts connections from localhost inside the container
CMD  ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

