#!/bin/bash

# IVIE Wedding Studio - Backend Startup Script
# This script is used by Render to start the backend service

echo "🚀 Starting IVIE Wedding Backend..."

# Set default values
PORT=${PORT:-8000}
WORKERS=${WEB_CONCURRENCY:-2}

# Wait for database to be ready (PostgreSQL)
echo "⏳ Waiting for database connection..."
sleep 3

# Run database initialization/migrations
echo "📦 Initializing database tables..."
python -c "from ung_dung.co_so_du_lieu import khoi_tao_csdl; khoi_tao_csdl()" || {
    echo "⚠️ Database initialization warning (may already exist)"
}

echo "✅ Database ready!"

# Start the application with Gunicorn (production)
echo "🌐 Starting Gunicorn server on port $PORT with $WORKERS workers..."

exec gunicorn ung_dung.chinh:ung_dung \
    --bind 0.0.0.0:$PORT \
    --workers $WORKERS \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout 120 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --log-level info
