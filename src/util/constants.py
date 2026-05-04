import json
import tempfile
from pathlib import Path
from src.util.self import get_my_ip

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parents[2]
log_dir = BASE_DIR / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
CONFIG_PATH = BASE_DIR / "config.json"


# --- Load config safely ---
with open(CONFIG_PATH, "r") as f:
    config: dict = json.load(f)

# --- Core settings ---
SIZE = config.get("max-space", 1024)
CMD = config.get("start-cmd", "py")

# --- Networking ---
networking: dict = config.get("networking", {})
PORT = networking.get("port", 9899)
PEERS = [(ip, int(port)) for ip, port in networking.get("peers", {}).items()] + [(get_my_ip(), PORT)]

# --- Temp / runtime ---
SYNC_TEMP_FOLDER = Path(tempfile.gettempdir()) / "sync-bridge"
SYNC_TEMP_FOLDER.mkdir(exist_ok=True)

REGISTRY_FILE = SYNC_TEMP_FOLDER / "registry.json"
