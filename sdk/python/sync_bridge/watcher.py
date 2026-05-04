import threading
import time


class Watcher:
    def __init__(self, bridge, interval=0.1):
        self.bridge = bridge
        self.interval = interval
        self.watching = {}
        self.running = False

    def watch(self, key, func):
        self.watching[key] = {
            "callback": func,
            "last": None
        }

    def _loop(self):
        while self.running:
            for key, meta in self.watching.items():
                try:
                    val = self.bridge.get(key)

                    if val != meta["last"]:
                        meta["last"] = val
                        meta["callback"](val)

                except Exception:
                    pass

            time.sleep(self.interval)

    def start(self):
        if self.running:
            return

        self.running = True
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()

    def stop(self):
        self.running = False