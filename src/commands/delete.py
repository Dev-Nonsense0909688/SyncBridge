from src.core.registry import VariableRegistry
from src.core.allocator import MemoryAllocator

def run(args):
    reg = VariableRegistry()
    mem = MemoryAllocator()

    meta = reg.get_key(args[1])
    if not meta:
        print("Key not found")
        return

    mem.free(meta["index"])
    del reg.data[args[1]]
    reg._save()