from src.core import Memory, VariableRegistry
from src.core.codec import decode
from src.util.constants import REGISTRY_FILE
from src.util.check_daemon import is_running


def run(args):
    if not is_running():
        print("Service not running. Use `serve` first.")
        return

    key = args[0]

    mem = Memory()
    reg = VariableRegistry(REGISTRY_FILE)

    data = reg.get_key(key)

    if not data:
        print(f"{key} → None")
        return

    ptr = data["index"]
    dtype = data["type"]

    value = decode(mem.read(ptr), dtype)

    print(f"{key} [{dtype}] = {value}")
