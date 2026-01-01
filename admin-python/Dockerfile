FROM python:3.11-slim

WORKDIR /app

# Install curl for health check
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create Streamlit config directory
RUN mkdir -p ~/.streamlit

# Streamlit config for production
RUN echo '\
[server]\n\
port = 8501\n\
address = "0.0.0.0"\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
serverAddress = "0.0.0.0"\n\
\n\
[theme]\n\
base = "dark"\n\
' > ~/.streamlit/config.toml

EXPOSE 8501

# Health check for Render
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "quan_tri.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
