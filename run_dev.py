from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


def main() -> None:
    """Start backend and frontend development servers."""

    backend_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.main:app",
        "--reload",
        "--reload-dir",
        "backend",
        "--reload-dir",
        "src",
    ]

    frontend_cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "frontend/app.py",
    ]

    print("Starting backend...")
    backend = subprocess.Popen(
        backend_cmd,
        cwd=PROJECT_ROOT,
    )

    print("Starting frontend...")
    frontend = subprocess.Popen(
        frontend_cmd,
        cwd=PROJECT_ROOT,
    )

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        backend.terminate()
        frontend.terminate()
        sys.exit(0)


if __name__ == "__main__":
    main()