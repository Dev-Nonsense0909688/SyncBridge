import socket
import threading
import logging
import json
from pathlib import Path
from logging.handlers import RotatingFileHandler

# ---------- PATH + LOGGING ----------
BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "sync-bridge.log"

logger = logging.getLogger("sync_bridge.p2p")
logger.setLevel(logging.DEBUG)

if not logger.handlers:  # prevent duplicate logs
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | [P2P] %(message)s")

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# ---------- P2P CLASS ----------
class P2P:
    def __init__(self, port: int, peers: list[tuple[str, int]], on_memory, on_json):
        self.port = port
        self.peers = peers
        self.on_memory = on_memory
        self.on_json = on_json

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))

        self.my_ip = self._get_my_ip()
        self.running = False

        logger.info(f"Initialized on {self.my_ip}:{self.port}")
        logger.info(f"Peers: {self.peers}")

    # ---------- UTILS ----------
    def _get_my_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
        finally:
            s.close()

    # ---------- RECEIVE ----------
    def _recv_loop(self):
        logger.info("[P2P] Receive loop started")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)

                # skip self messages
                if addr[0] == self.my_ip:
                    continue

                if not data:
                    continue

                msg_type = data[:1]
                payload = data[1:]

                if msg_type == b"M":
                    self.on_memory(payload, addr)

                elif msg_type == b"J":
                    try:
                        obj = json.loads(payload.decode())
                        self.on_json(obj, addr)
                    except Exception as e:
                        logger.warning(f"Invalid JSON from {addr}: {e}")

            except Exception as e:
                logger.error(f"[P2P] Recv error: {e}")

    def start(self):
        if self.running:
            return

        self.running = True
        threading.Thread(target=self._recv_loop, daemon=True).start()
        logger.info("P2P started")

    def stop(self):
        self.running = False
        try:
            self.sock.close()
        except:
            pass
        logger.info("P2P stopped")

    # ---------- SEND ----------
    def send_memory(self, data: bytes):
        for peer in self.peers:
            try:
                self.sock.sendto(b"M" + data, peer)
            except Exception as e:
                logger.error(f"[P2P] Send memory error {peer}: {e}")

    def send_json(self, obj: dict):
        try:
            payload = json.dumps(obj).encode()
        except Exception as e:
            logger.error(f"[P2P] JSON encode error: {e}")
            return

        for peer in self.peers:
            try:
                self.sock.sendto(b"J" + payload, peer)
            except Exception as e:
                logger.error(f"[P2P] Send json error {peer}: {e}")
