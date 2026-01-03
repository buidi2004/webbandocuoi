# IVIE Wedding Studio - Backend Dockerfile
# Python 3.12 Slim for Pydantic v2 compatibility

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Fix line endings (CRLF to LF) for shell scripts
RUN dos2unix start.sh && chmod +x start.sh

# Create directory for file uploads
RUN mkdir -p tep_tin && chmod 755 tep_tin

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run the application
CMD ["./start.sh"]
