#!/bin/bash

# IVIE Wedding Studio - Backend Startup Script (FREE TIER OPTIMIZED)
# Tối ưu cho Render Free Tier: 512MB RAM, 1 worker

# Exit immediately if a command exits with a non-zero status
set -e

echo "=================================================="
echo "🚀 STARTING IVIE WEDDING BACKEND (FREE TIER)"
echo "=================================================="
date

# Debug: Print system info
echo "📂 Current Directory: $(pwd)"
echo "📂 Directory Contents:"
ls -la

echo "🐍 Python Version:"
python --version

echo "📦 Installed Packages (Key components):"
pip list | grep -E "fastapi|uvicorn|gunicorn|sqlalchemy|psycopg2" || echo "Packages checking skipped"

# Set default values - OPTIMIZED FOR FREE TIER
PORT=${PORT:-8000}
WORKERS=${WEB_CONCURRENCY:-1}
TIMEOUT=${GUNICORN_TIMEOUT:-60}
MAX_REQUESTS=${MAX_REQUESTS:-500}
MAX_REQUESTS_JITTER=${MAX_REQUESTS_JITTER:-50}

echo "⚙️  Configuration (FREE TIER OPTIMIZED):"
echo "   - PORT: $PORT"
echo "   - WORKERS: $WORKERS (optimized for 512MB RAM)"
echo "   - TIMEOUT: ${TIMEOUT}s (reduced for faster response)"
echo "   - MAX_REQUESTS: $MAX_REQUESTS (restart worker to free memory)"
# Mask credentials in logs
if [ ! -z "$DATABASE_URL" ]; then
    echo "   - DATABASE_URL: ${DATABASE_URL:0:15}... (connected)"
else
    echo "   - DATABASE_URL: Not set (will use SQLite fallback)"
fi

# Wait for database to be ready (PostgreSQL)
echo "⏳ Waiting for database connection..."
sleep 5

# Run database initialization/migrations
echo "📦 Initializing database tables..."
# Run with error handling
if python -c "
try:
    from ung_dung.co_so_du_lieu import khoi_tao_csdl
    print('🔄 Calling khoi_tao_csdl()...')
    khoi_tao_csdl()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'⚠️  Database initialization warning: {e}')
    print('Tables may already exist. Continuing...')
"; then
    echo "✅ Database setup completed"
else
    echo "⚠️  Database setup warning. Continuing with startup..."
fi

# Create upload directory if not exists
mkdir -p tep_tin
chmod 755 tep_tin
echo "📁 Upload directory ready: ./tep_tin"

# Try Gunicorn first (production), fallback to Uvicorn
echo "🌐 Starting server with optimized settings..."

if command -v gunicorn &> /dev/null; then
    echo "✅ Gunicorn found. Starting with FREE TIER optimization..."
    echo "   → 1 worker (saves RAM)"
    echo "   → 60s timeout (faster response)"
    echo "   → Auto-restart after 500 requests (memory cleanup)"

    # Run Gunicorn with FREE TIER optimizations
    exec gunicorn ung_dung.chinh:ung_dung \
        --bind 0.0.0.0:$PORT \
        --workers $WORKERS \
        --worker-class uvicorn.workers.UvicornWorker \
        --timeout $TIMEOUT \
        --keep-alive 5 \
        --max-requests $MAX_REQUESTS \
        --max-requests-jitter $MAX_REQUESTS_JITTER \
        --worker-tmp-dir /dev/shm \
        --access-logfile - \
        --error-logfile - \
        --capture-output \
        --log-level info \
        --preload
else
    echo "⚠️  Gunicorn not found. Falling back to Uvicorn..."
    echo "   → Running with $WORKERS worker(s)"

    # Run Uvicorn with FREE TIER optimizations
    exec uvicorn ung_dung.chinh:ung_dung \
        --host 0.0.0.0 \
        --port $PORT \
        --workers $WORKERS \
        --log-level info \
        --timeout-keep-alive 5 \
        --limit-concurrency 100 \
        --backlog 50
fi
