from src.core.registry import VariableRegistry
from src.core.allocator import MemoryAllocator

def cmd_del(args):
    reg = VariableRegistry()
    mem = MemoryAllocator()

    meta = reg.get_key(args.key)
    if not meta:
        print("Key not found")
        return

    mem.free(meta["index"])
    del reg.data[args.key]
    reg._save()