# ============================================
# IVIE Wedding Studio - Admin Panel Dockerfile
# FREE TIER OPTIMIZED for Render (512MB RAM)
# ============================================
# Streamlit Admin Dashboard with Python 3.11
# Build time: ~3-4 minutes
# Runtime RAM: ~150-200MB (optimized)

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Environment variables - optimized for free tier
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_FILE_WATCHER_TYPE=none \
    STREAMLIT_SERVER_MAX_UPLOAD_SIZE=3 \
    STREAMLIT_SERVER_MAX_MESSAGE_SIZE=50

# Install system dependencies (minimal)
# curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy application code
COPY . .

# Create Streamlit config directory
RUN mkdir -p ~/.streamlit

# Create Streamlit config for production - FREE TIER OPTIMIZED
RUN echo '[server]\n\
port = 8501\n\
address = "0.0.0.0"\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
maxUploadSize = 3\n\
maxMessageSize = 50\n\
fileWatcherType = "none"\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
serverAddress = "0.0.0.0"\n\
\n\
[theme]\n\
base = "dark"\n\
primaryColor = "#b59410"\n\
backgroundColor = "#0e1117"\n\
secondaryBackgroundColor = "#262730"\n\
textColor = "#fafafa"\n\
\n\
[client]\n\
showErrorDetails = false\n\
toolbarMode = "minimal"\n\
\n\
[runner]\n\
magicEnabled = false\n\
fastReruns = true\n\
' > ~/.streamlit/config.toml

# Create credentials file to disable telemetry
RUN echo '[general]\n\
email = ""\n\
' > ~/.streamlit/credentials.toml

# Expose Streamlit port
EXPOSE 8501

# Health check for Render - optimized
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app with optimized settings
# Using quan_tri_optimized_v2.py for faster startup and lower memory
CMD ["streamlit", "run", "quan_tri_optimized_v2.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.fileWatcherType=none", \
     "--server.maxUploadSize=3", \
     "--server.maxMessageSize=50", \
     "--browser.gatherUsageStats=false", \
     "--client.toolbarMode=minimal"]

# ============================================
# FREE TIER OPTIMIZATION NOTES
# ============================================
# 1. File watcher disabled to save RAM
#    - Saves ~30-50MB RAM
#    - No auto-reload in production (not needed)
#
# 2. Max upload size reduced to 3MB
#    - Prevents OOM when uploading files
#    - Still enough for most images
#
# 3. Max message size reduced to 50MB
#    - Limits WebSocket message size
#    - Prevents memory spikes
#
# 4. Magic commands disabled
#    - Reduces processing overhead
#    - Saves CPU and RAM
#
# 5. Fast reruns enabled
#    - Quicker response time
#    - Better UX on free tier
#
# 6. Using quan_tri_optimized_v2.py
#    - Lazy loading of modules
#    - Reduces startup time
#    - Lower memory footprint
#
# Expected resource usage on Render Free Tier:
# - Build time: 3-4 minutes
# - Image size: ~400MB
# - Runtime RAM: 150-200MB
# - Cold start: ~30-40 seconds after sleep
#
# Alternative startup (if quan_tri_optimized_v2.py not available):
# CMD ["streamlit", "run", "quan_tri.py", ...]
