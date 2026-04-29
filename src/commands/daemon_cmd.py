import os
import subprocess
import signal
import sys
from pathlib import Path
from src.utils.config import PID_FILE, PLATFORM, REG_FILE, NET_PID_FILE, PORT, BASE_DIR


# ---------- utils ----------
def _kill_pid(pid):
    try:
        if PLATFORM == "win32":
            subprocess.call(
                ["taskkill", "/PID", str(pid), "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            os.kill(pid, signal.SIGTERM)
    except Exception:
        pass


def _is_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except Exception:
        return False


# ---------- START ----------
def cmd_up(args):
    py = sys.executable

    # ---- tunnel (both OS) ----
    if os.path.exists(NET_PID_FILE):
        try:
            pid = int(open(NET_PID_FILE).read())
            if _is_alive(pid):
                print("Tunnel already running")
            else:
                os.remove(NET_PID_FILE)
                raise Exception()
        except:
            proc_net = subprocess.Popen(
                [py, f"{BASE_DIR}/daemon/tunnel.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            with open(NET_PID_FILE, "w") as f:
                f.write(str(proc_net.pid))
            print(f"Tunnel started on port {PORT} (PID: {proc_net.pid})")
    else:
        proc_net = subprocess.Popen(
            [py, f"{BASE_DIR}/daemon/tunnel.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        with open(NET_PID_FILE, "w") as f:
            f.write(str(proc_net.pid))
        print(f"Tunnel started on port {PORT} (PID: {proc_net.pid})")

    # ---- memory daemon (Windows only) ----
    if PLATFORM == "win32":
        if os.path.exists(PID_FILE):
            try:
                pid = int(open(PID_FILE).read())
                if _is_alive(pid):
                    print("Memory daemon already running")
                    return
                else:
                    os.remove(PID_FILE)
            except:
                pass

        proc_mem = subprocess.Popen(
            [py, f"{BASE_DIR}/daemon/windows_mem.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        with open(PID_FILE, "w") as f:
            f.write(str(proc_mem.pid))

        print(f"Memory daemon started (PID: {proc_mem.pid})")

    print("Daemon started")


# ---------- STOP ----------
def cmd_down(args):
    # ---- stop tunnel ----
    if os.path.exists(NET_PID_FILE):
        try:
            pid = int(open(NET_PID_FILE).read())
            _kill_pid(pid)
            os.remove(NET_PID_FILE)
            print(f"Tunnel stopped (PID: {pid})")
        except Exception as e:
            print(f"Tunnel stop error: {e}")
    else:
        print("Tunnel not running")

    # ---- stop memory daemon (Windows only) ----
    if PLATFORM == "win32":
        if os.path.exists(PID_FILE):
            try:
                pid = int(open(PID_FILE).read())
                _kill_pid(pid)
                os.remove(PID_FILE)
                print(f"Memory daemon stopped (PID: {pid})")
            except Exception as e:
                print(f"Memory stop error: {e}")
        else:
            print("Memory daemon not running")

    # ---- cleanup ----
    if os.path.exists(REG_FILE):
        try:
            os.remove(REG_FILE)
        except:
            pass

    print("Daemon stopped")