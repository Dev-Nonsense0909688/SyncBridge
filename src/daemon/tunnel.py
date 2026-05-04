import time
import logging
from logging.handlers import RotatingFileHandler
import json

from src.networking.p2p import P2P
from src.core.memory import Memory 
from src.util.constants import REGISTRY_FILE, PORT, PEERS, SIZE


# ---------- LOGGING ----------
logger = logging.getLogger("sync_bridge")
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler(
    f"./logs/sync-bridge.log",
    maxBytes=1_000_000,
    backupCount=3
)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)


# ---------- MEMORY ----------
mm = Memory()

last = None
last_remote = None


# ---------- callbacks ----------
def on_memory(data, addr):
    global last_remote

    logger.info(f"[MEMORY] from {addr} -> {len(data)} bytes")

    last_remote = data
    mm.mm[:len(data)] = data

import os

def on_json(obj, addr):
    logger.info(f"[JSON] from {addr} -> {obj}")
    try:
        tmp = REGISTRY_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(obj, f, indent=2)
        os.replace(tmp, REGISTRY_FILE)
    except Exception as e:
        logger.error(f"[JSON]{e}")
        
# ---------- setup ----------

p2p = P2P(PORT, PEERS, on_memory, on_json)
p2p.start()

logger.info("mmap sync started")


# ---------- sync loop ----------
print(f"Starting p2p tunnel on port: {PORT}")
print(f"Member peers: {PEERS}")
last = bytes(mm.mm[:SIZE])

while True:
    try:
        current = bytes(mm.mm[:SIZE])

        # avoid echo loop
        if current != last and current != last_remote:
            logger.debug(f"memory changed, sending {len(current)} bytes")
            p2p.send_memory(current)
            p2p.send_json(json.load(open(REGISTRY_FILE, "r")))
            last = current

        time.sleep(0.05)

    except KeyboardInterrupt:
        logger.info("stopped by user")
        break

    except Exception as e:
        logger.error(f"loop error: {e}")