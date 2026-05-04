import time
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.networking.p2p import P2P
from src.core.memory import Memory
from src.util.constants import REGISTRY_FILE, PORT, PEERS, SIZE, BASE_DIR

# ---------- PATHS ----------
BASE_DIR = Path(BASE_DIR)
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "sync-bridge.log"


# ---------- LOGGING ----------
logger = logging.getLogger("sync_bridge")
logger.setLevel(logging.DEBUG)

# file handler
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
)

# console handler (PRINTS LOGS)
console_handler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ---------- MEMORY ----------
mm = Memory()
last = None
last_remote = None


# ---------- HELPERS ----------
def safe_read_json():
    try:
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"[TUNNEL][JSON READ ERROR] {e}")
        return None


# ---------- CALLBACKS ----------
def on_memory(data, addr):
    global last_remote

    logger.info(f"[TUNNEL][MEMORY] {addr} -> {len(data)} bytes")

    last_remote = data
    mm.mm[: len(data) - 1] = data


def on_json(obj, addr):
    logger.info(f"[TUNNEL][JSON] {addr} -> update")

    try:
        tmp = str(REGISTRY_FILE) + ".tmp"

        with open(tmp, "w") as f:
            json.dump(obj, f, indent=2)

        Path(tmp).replace(REGISTRY_FILE)

    except Exception as e:
        logger.error(f"[TUNNEL][JSON ERROR] {e}")


# ---------- SETUP ----------

p2p = P2P(PORT, PEERS, on_memory, on_json)
p2p.start()


# ---------- SYNC LOOP ----------
last = bytes(mm.mm[:SIZE])
last_json_hash = None
last_send_time = time.time()

while True:
    try:
        current = bytes(mm.mm[:SIZE])

        # ---- MEMORY SYNC ----
        if current != last and current != last_remote:
            logger.debug(f"[TUNNEL][SYNC] memory -> {len(current)} bytes")

            p2p.send_memory(current)
            last = current
            last_send_time = time.time()

        # ---- JSON SYNC ----
        obj = safe_read_json()
        if obj is not None:
            current_hash = hash(json.dumps(obj, sort_keys=True))

            if current_hash != last_json_hash:
                logger.debug("[TUNNEL][SYNC] json changed")

                p2p.send_json(obj)
                last_json_hash = current_hash

        time.sleep(0.05)

    except KeyboardInterrupt:
        logger.info("stopped by user")
        break

    except Exception as e:
        logger.error(f"[TUNNEL][LOOP ERROR] {e}")
        time.sleep(1)
