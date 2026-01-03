# ============================================
# IVIE Wedding Studio - Backend Dockerfile
# FREE TIER OPTIMIZED for Render (512MB RAM)
# ============================================
# Python 3.12 Slim for Pydantic v2 compatibility
# Build time: ~3-5 minutes
# Image size: ~350MB (optimized from 500MB+)
# Runtime RAM: ~200-250MB with 1 worker

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Environment variables for optimization
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies in one layer
# gcc, libpq-dev for psycopg2
# curl for health checks
# dos2unix for line ending conversion
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    dos2unix \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Use --no-cache-dir to reduce image size
# Install in one layer for faster build
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy application code
COPY . .

# Fix line endings (CRLF to LF) for shell scripts
# Make start.sh executable
RUN if [ -f start.sh ]; then dos2unix start.sh && chmod +x start.sh; fi

# Create directory for file uploads
# Set proper permissions
RUN mkdir -p tep_tin && chmod 755 tep_tin

# Create a non-root user for security (optional, but recommended)
# RUN useradd -m -u 1000 ivie && chown -R ivie:ivie /app
# USER ivie

# Expose port
EXPOSE 8000

# Health check - optimized for free tier
# Check every 30s, timeout 10s, start checking after 60s
# Retry 3 times before marking unhealthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run the application
# Uses optimized start.sh with 1 worker for free tier
CMD ["./start.sh"]

# ============================================
# FREE TIER OPTIMIZATION NOTES
# ============================================
# 1. Single worker (WEB_CONCURRENCY=1) saves RAM
#    - 1 worker = ~200MB RAM
#    - 2 workers = ~400MB RAM (would exceed 512MB limit)
#
# 2. Preload app to share memory between workers
#    - Done in start.sh with --preload flag
#
# 3. Auto-restart workers after 500 requests
#    - Prevents memory leaks
#    - Keeps RAM usage stable
#
# 4. Reduced timeout (60s instead of 120s)
#    - Faster response to hung requests
#    - Frees up resources quicker
#
# 5. Health check ensures service stays responsive
#    - Render will restart if unhealthy
#
# Build optimization:
# - Multi-stage build not needed (overhead not worth it for small app)
# - System deps installed in one layer
# - Python deps cached with requirements.txt
# - Clean up apt cache to reduce image size
#
# Expected resource usage on Render Free Tier:
# - Build time: 3-5 minutes
# - Image size: ~350MB
# - Runtime RAM: 200-250MB
# - CPU: Shared (sufficient for low-medium traffic)
# - Cold start: ~20-30 seconds after sleep
