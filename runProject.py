import os
import subprocess
import sys
import platform
from pathlib import Path

# === CONFIGURATION ===
BACKEND_DIR = Path("backend")
FRONTEND_DIR = Path("frontend")
PYTHON = sys.executable
NODE_COMMAND = "npm.cmd" if platform.system() == "Windows" else "npm"

# === COLORS FOR OUTPUT ===
class c:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"

def print_status(message, color=c.OKBLUE):
    print(f"{color}[*] {message}{c.ENDC}")

def run_command(command, cwd=None):
    """Runs a shell command and handles errors gracefully."""
    try:
        subprocess.check_call(command, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"{c.FAIL}[!] Command failed: {command}{c.ENDC}")
        sys.exit(1)

def ensure_backend_deps():
    print_status("Checking and installing backend dependencies...", c.OKBLUE)
    requirements = [
        "fastapi",
        "uvicorn",
        "scapy",
        "pydantic",
        "python-multipart",
        "colorlog"
    ]
    for pkg in requirements:
        subprocess.run(f"{PYTHON} -m pip install {pkg}", shell=True, cwd=BACKEND_DIR)

def ensure_frontend_deps():
    print_status("Checking and installing frontend dependencies...", c.OKBLUE)
    package_json = FRONTEND_DIR / "package.json"
    if not package_json.exists():
        print(f"{c.FAIL}[!] package.json not found in {FRONTEND_DIR}{c.ENDC}")
        sys.exit(1)
    run_command(f"{NODE_COMMAND} install", cwd=FRONTEND_DIR)

def start_backend():
    print_status("Starting FastAPI backend on http://127.0.0.1:8000 ...", c.OKGREEN)
    return subprocess.Popen(f"{PYTHON} -m uvicorn app.main:app --reload", cwd=BACKEND_DIR, shell=True)

def start_frontend():
    print_status("Starting React frontend on http://127.0.0.1:8080 ...", c.OKGREEN)
    return subprocess.Popen(f"{NODE_COMMAND} run dev", cwd=FRONTEND_DIR, shell=True)

def main():
    print(f"{c.HEADER}\n=== UDON Intrusion Detection System Launcher ==={c.ENDC}")

    # 1. Verify folder structure
    if not BACKEND_DIR.exists() or not FRONTEND_DIR.exists():
        print(f"{c.FAIL}[!] Missing 'backend/' or 'frontend/' directories.{c.ENDC}")
        sys.exit(1)

    # 2. Install dependencies
    ensure_backend_deps()
    ensure_frontend_deps()

    # 3. Launch both servers
    backend_process = start_backend()
    frontend_process = start_frontend()

    print_status("Both servers are running. Press CTRL+C to stop.", c.OKGREEN)
    print_status("Backend → http://127.0.0.1:8000/docs")
    print_status("Frontend → http://127.0.0.1:8080")

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print_status("Shutting down servers...", c.WARNING)
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
