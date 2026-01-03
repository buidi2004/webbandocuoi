# IVIE Wedding Studio - Admin Panel Dockerfile
# Streamlit Admin Dashboard with Python 3.11

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create Streamlit config directory
RUN mkdir -p ~/.streamlit

# Create Streamlit config for production
RUN echo '[server]\n\
port = 8501\n\
address = "0.0.0.0"\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
maxUploadSize = 50\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
serverAddress = "0.0.0.0"\n\
\n\
[theme]\n\
base = "dark"\n\
primaryColor = "#b59410"\n\
\n\
[client]\n\
showErrorDetails = false\n\
toolbarMode = "minimal"\n\
' > ~/.streamlit/config.toml

# Expose Streamlit port
EXPOSE 8501

# Health check for Render
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
# Using quan_tri_optimized_v2.py for faster startup (lazy loading)
# Alternative: quan_tri.py for full version
CMD ["streamlit", "run", "quan_tri_optimized_v2.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
