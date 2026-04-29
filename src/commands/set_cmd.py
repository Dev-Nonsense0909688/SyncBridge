from src.core.allocator import MemoryAllocator
from src.core.registry import VariableRegistry
from src.core.types import encode
from src.utils.parser import parse

def cmd_set(args):
    key = args.key
    val = parse(args.value)

    encoded, dtype = encode(val)

    mem = MemoryAllocator()
    reg = VariableRegistry()

    existing = reg.get_key(key)

    if existing:
        ptr = mem.write(existing["index"], encoded)
    else:
        ptr = mem.alloc(len(encoded))
        mem.write(ptr, encoded)

    reg.set_key(key, {
        "index": ptr,
        "type": dtype,
        "size": len(encoded)
    })