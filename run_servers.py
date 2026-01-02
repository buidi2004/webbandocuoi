#!/usr/bin/env python
"""
IVIE Wedding Studio - Run Both Servers
Chạy cả Backend API và Admin Panel cùng lúc
"""

import os
import subprocess
import sys
import time
import webbrowser
from threading import Thread


def run_backend():
    """Chạy Backend API Server"""
    os.chdir(os.path.join(os.path.dirname(__file__), "backend"))
    subprocess.run(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "ung_dung.chinh:ung_dung",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
            "--reload",
        ]
    )


def run_admin():
    """Chạy Admin Panel"""
    os.chdir(os.path.join(os.path.dirname(__file__), "admin-python"))
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "quan_tri.py",
            "--server.port",
            "8501",
            "--server.address",
            "127.0.0.1",
        ]
    )


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║          IVIE WEDDING STUDIO - SERVER MANAGER             ║
╚═══════════════════════════════════════════════════════════╝
    """)

    # Start backend in a thread
    print("[1/2] Đang khởi động Backend API (port 8000)...")
    backend_thread = Thread(target=run_backend, daemon=True)
    backend_thread.start()

    # Wait for backend to start
    time.sleep(3)

    # Start admin in a thread
    print("[2/2] Đang khởi động Admin Panel (port 8501)...")
    admin_thread = Thread(target=run_admin, daemon=True)
    admin_thread.start()

    # Wait for admin to start
    time.sleep(5)

    print("""
╔═══════════════════════════════════════════════════════════╗
║                    SERVERS STARTED!                       ║
╠═══════════════════════════════════════════════════════════╣
║  Backend API:    http://localhost:8000                    ║
║  API Docs:       http://localhost:8000/docs               ║
║  Admin Panel:    http://localhost:8501                    ║
╠═══════════════════════════════════════════════════════════╣
║  Nhấn Ctrl+C để dừng tất cả servers                       ║
╚═══════════════════════════════════════════════════════════╝
    """)

    # Open browser
    webbrowser.open("http://localhost:8501")

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Đang dừng servers...")
        sys.exit(0)


if __name__ == "__main__":
    main()
