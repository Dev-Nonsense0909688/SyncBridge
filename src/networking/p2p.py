import socket
import threading
import logging
from logging.handlers import RotatingFileHandler
import json
from src.utils.config import PLATFORM

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

    def _get_my_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        finally:
            s.close()

    # ---------------- RECEIVE ----------------
    def _recv_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(65535)

                if addr[0] == self.my_ip:
                    continue

                msg_type = data[:1]
                payload = data[1:]

                if msg_type == b"M":
                    self.on_memory(payload, addr)

                elif msg_type == b"J":
                    try:
                        obj = json.loads(payload.decode())
                        self.on_json(obj, addr)
                    except:
                        pass

            except Exception as e:
                logger.error(f"[P2P] Recv error: {e}")

    def start(self):
        self.running = True
        threading.Thread(target=self._recv_loop, daemon=True).start()

    # ---------------- SEND ----------------
    def send_memory(self, data: bytes):
        for peer in self.peers:
            try:
                self.sock.sendto(b"M" + data, peer)
            except Exception as e:
                logger.error(f"[P2P] Send memory error {peer}: {e}")

    def send_json(self, obj: dict):
        try:
            payload = json.dumps(obj).encode()
        except:
            return

        for peer in self.peers:
            try:
                self.sock.sendto(b"J" + payload, peer)
            except Exception as e:
                logger.error(f"[P2P] Send json error {peer}: {e}")