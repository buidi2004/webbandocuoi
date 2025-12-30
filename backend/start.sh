#!/bin/bash
# Script khởi động backend - chạy migration trước khi start server

echo "🔄 Đang chạy migration..."
python migrate_combo.py

echo "🚀 Khởi động server..."
uvicorn ung_dung.chinh:ung_dung --host 0.0.0.0 --port 8000
