import sys
import importlib
from typing import List


def main(argv: List[str] = None) -> None:
    argv = argv or sys.argv[1:]

    if not argv:
        print("Usage: <command> [args]")
        sys.exit(1)

    cmd, *args = argv

    try:
        module = importlib.import_module(f"src.commands.{cmd}")
    except ModuleNotFoundError:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

    if not hasattr(module, "run"):
        print(f"Command '{cmd}' is missing a 'run' entrypoint")
        sys.exit(1)

    try:
        module.run(args)
    except Exception as e:
        print(f"Error executing '{cmd}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()