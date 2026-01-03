#!/bin/bash

# IVIE Wedding Studio - Backend Startup Script
# This script is used by Render to start the backend service

# Exit immediately if a command exits with a non-zero status
set -e

echo "=================================================="
echo "🚀 STARTING IVIE WEDDING BACKEND"
echo "=================================================="
date

# Debug: Print system info
echo "📂 Current Directory: $(pwd)"
echo "📂 Directory Contents:"
ls -la

echo "🐍 Python Version:"
python --version

echo "📦 Installed Packages (Key components):"
pip list | grep -E "fastapi|uvicorn|gunicorn|sqlalchemy|psycopg2"

# Set default values
PORT=${PORT:-8000}
WORKERS=${WEB_CONCURRENCY:-2}

echo "⚙️  Configuration:"
echo "   - PORT: $PORT"
echo "   - WORKERS: $WORKERS"
# Mask credentials in logs
echo "   - DATABASE_URL: ${DATABASE_URL:0:15}..."

# Wait for database to be ready (PostgreSQL)
echo "⏳ Waiting for database connection..."
sleep 3

# Run database initialization/migrations
echo "📦 Initializing database tables..."
# We run this with full output to see errors if any
if python -c "from ung_dung.co_so_du_lieu import khoi_tao_csdl; print('Calling khoi_tao_csdl()...'); khoi_tao_csdl(); print('Done.')"; then
    echo "✅ Database initialized successfully"
else
    echo "⚠️ Database initialization warning (Tables may already exist). Continuing..."
fi

# Try Gunicorn first (production), fallback to Uvicorn
echo "🌐 Starting server..."

if command -v gunicorn &> /dev/null; then
    echo "✅ Gunicorn found. Starting with $WORKERS workers..."

    # Run Gunicorn
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
else
    echo "⚠️ Gunicorn not found. Falling back to Uvicorn..."

    # Run Uvicorn
    exec uvicorn ung_dung.chinh:ung_dung \
        --host 0.0.0.0 \
        --port $PORT \
        --workers $WORKERS \
        --log-level info
fi
