from src.core import Memory, VariableRegistry
from src.core.codec import encode, decode
from .watcher import Watcher

class SyncBridge:
    def __init__(self):
        self.mem = Memory()
        self.reg = VariableRegistry("registry.json")
        self._watcher = Watcher(self)
        self._watcher.start()

    def set(self, key: str, val):
        ptr = self.mem.alloc()
        data, typ = encode(val)

        self.mem.write(ptr, data)
        self.reg.set_key(key, {"index": ptr, "type": typ})

    def get(self, key: str):
        meta = self.reg.get_key(key)
        data = self.mem.read(meta["index"])
        return decode(data, meta["type"])

    def watch(self, key, func):
        self._watcher.watch(key, func)