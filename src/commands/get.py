from src.core.allocator import MemoryAllocator
from src.core.registry import VariableRegistry
from src.core.types import decode

def run(args):
    reg = VariableRegistry()
    mem = MemoryAllocator()

    meta = reg.get_key(args[0])
    if not meta:
        print("Key not found")
        return

    raw = mem.read(meta["index"], meta["size"])
    print(decode(raw, meta["type"]))