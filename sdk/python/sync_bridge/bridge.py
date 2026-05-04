from src.core import Memory, VariableRegistry
from src.core.codec import encode, decode
from src.util.constants import REGISTRY_FILE
from .watcher import Watcher

class Variable:
    def __init__(self, name: str):
        self.key = name
        self.mem = Memory()
        self.reg = VariableRegistry(REGISTRY_FILE)
        self._watcher = Watcher(self)
        self._watcher.start()

    def set(self, val):
        ptr = self.mem.alloc()
        data, typ = encode(val)

        self.mem.write(ptr, data)
        self.reg.set_key(self.key, {"index": ptr, "type": typ})

    def get(self):
        meta = self.reg.get_key(self.key)
        data = self.mem.read(meta["index"])
        return decode(data, meta["type"])

    def watch(self, key, func):
        self._watcher.watch(key, func)


class SyncBridge:
    def __init__(self):
        pass

    def bind(self, name: str):
        return Variable(name)

    
