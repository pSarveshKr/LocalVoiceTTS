import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path


HOST = "127.0.0.1"
PORT = 8000
APP_URL = f"http://{HOST}:{PORT}/app"


def wait_for_backend(timeout_seconds: int = 30) -> bool:
    deadline = time.time() + timeout_seconds
    health_url = f"http://{HOST}:{PORT}/health"

    while time.time() < deadline:
        try:
            with urllib.request.urlopen(health_url, timeout=1) as response:
                return response.status == 200
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.4)

    return False


def main() -> int:
    root = Path(__file__).resolve().parent
    backend = root / "backend"

    print("=" * 50)
    print("LocalVoice TTS starting")
    print("=" * 50)

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            HOST,
            "--port",
            str(PORT),
        ],
        cwd=backend,
    )

    try:
        if wait_for_backend():
            print(f"Opening {APP_URL}")
            webbrowser.open(APP_URL)
            print("App ready. Press Ctrl+C to stop.")
        else:
            print("Backend did not respond in time. Check the terminal output above.")
            return 1

        process.wait()
    except KeyboardInterrupt:
        print("\nStopping LocalVoice TTS...")
        process.terminate()
        process.wait(timeout=10)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
