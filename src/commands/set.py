from src.core import Memory, VariableRegistry
from src.core.codec import encode
from src.util.constants import REGISTRY_FILE
from src.util.check_daemon import is_running
from src.util.parser import parse


def run(args):
    if not is_running():
        print("Service not running. Use `serve` first.")
        return

    key, raw_val = args
    val = parse(raw_val)

    mem = Memory()
    reg = VariableRegistry(REGISTRY_FILE)

    encoded_val, val_type = encode(val)
    data = reg.get_key(key)

    if not data:
        ptr = mem.alloc()
        action = "Created"
    else:
        ptr = data["index"]
        action = "Updated"

    mem.write(ptr, encoded_val)
    reg.set_key(key, {"index": ptr, "type": val_type})

    print(f"{action} → {key} [{val_type}] = {val}")
