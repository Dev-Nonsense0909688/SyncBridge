import json
import tempfile
import os
import socket
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = BASE_DIR.parent / "bridge.json"

def _get_my_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        finally:
            s.close()

try:
    data = json.load(open(CONFIG_PATH, "r"))
except:
    raise ValueError("Error loadig config data")


HEADER_SIZE = 9
PLATFORM = sys.platform    
PID_FILE = os.path.join(tempfile.gettempdir(), "sync_bridge.pid")
NET_PID_FILE = os.path.join(tempfile.gettempdir(), "sync_bridge_networking.pid")
REG_FILE = os.path.join(tempfile.gettempdir(), "sync_bridge.json")

PORT = data["settings"].get("port")
SIZE = data["settings"].get("max-space")
NAME = data["settings"].get("name")

PEERS = [(ip, port) for ip, port in data["peers"].items()] + [(str(_get_my_ip()), PORT)]