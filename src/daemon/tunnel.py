import time
import logging
from logging.handlers import RotatingFileHandler
import json

from src.networking.p2p import P2P
from src.core.allocator import MemoryAllocator 
from src.utils.config import PLATFORM, REG_FILE


# ---------- LOGGING ----------
logger = logging.getLogger("sync_bridge")
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler(
    f"./logs/sync-{PLATFORM}.log",
    maxBytes=1_000_000,
    backupCount=3
)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)


# ---------- MEMORY ----------
mm = MemoryAllocator()

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
        tmp = REG_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(obj, f, indent=2)
        os.replace(tmp, REG_FILE)
    except Exception as e:
        logger.error(f"[JSON]{e}")
        
# ---------- setup ----------

peers = [
    ("192.168.29.211", 9899),
    ("192.168.29.205", 9899),
]

p2p = P2P(9899, peers, on_memory, on_json)
p2p.start()

logger.info("mmap sync started")


# ---------- sync loop ----------
last = bytes(mm.mm[:2048])

while True:
    try:
        current = bytes(mm.mm[:2048])

        # avoid echo loop
        if current != last and current != last_remote:
            logger.debug(f"memory changed, sending {len(current)} bytes")
            p2p.send_memory(current)
            p2p.send_json(json.load(open(REG_FILE, "r")))
            last = current

        time.sleep(0.05)

    except KeyboardInterrupt:
        logger.info("stopped by user")
        break

    except Exception as e:
        logger.error(f"loop error: {e}")