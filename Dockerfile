FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps required by some packages (git, build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

# Use a non-root user for security
RUN groupadd --system appgroup && useradd --system --gid appgroup --create-home appuser || true

# Create the generated_tasks directory and give ownership to appuser
RUN mkdir -p /app/generated_tasks && chown -R appuser:appgroup /app

USER appuser

# Expose the port Spaces will route to (use PORT env variable default 8080)
EXPOSE 8080
ENV PORT=8080

# Start Uvicorn; allow PORT override from environment (used by Spaces)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
