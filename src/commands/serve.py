import subprocess
import threading
import os
from pathlib import Path
import json
from src.util.constants import BASE_DIR, REGISTRY_FILE, CMD
from src.util.check_daemon import is_running


def stream(pipe):
    try:
        for line in iter(pipe.readline, ''):
            print(line, end='')
    finally:
        pipe.close()


def start_process(path: Path):
    proc = subprocess.Popen(
        [CMD, "-u", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    threading.Thread(target=stream, args=(proc.stdout,), daemon=True).start()
    threading.Thread(target=stream, args=(proc.stderr,), daemon=True).start()

    return proc


def run(args):
    server_path = Path(BASE_DIR) / "src" / "daemon" / "server.py"
    tunnel_path = Path(BASE_DIR) / "src" / "daemon" / "tunnel.py"
    os.makedirs(Path(BASE_DIR) / "logs", exist_ok = True)
    json.dump({},open(REGISTRY_FILE, "w"), indent=2)
    if is_running():
        print("Already running")
        return

    procs = []

    try:
        procs.append(start_process(server_path))
        procs.append(start_process(tunnel_path))

        # wait for both
        for p in procs:
            p.wait()

    except KeyboardInterrupt:
        print("\nShutting down...")

        for p in procs:
            p.terminate()

        for p in procs:
            p.wait()

        if os.path.exists(REGISTRY_FILE):
            os.remove(REGISTRY_FILE)

