from pathlib import Path
from typing import List
from src.utils.config import BASE_DIR, PLATFORM

LOG_PATH = Path(BASE_DIR).parent / f"sync-{PLATFORM}.log"


def clear_cmd() -> None:
    if LOG_PATH.exists():
        LOG_PATH.write_text("")
        print("Logs cleared.")
    else:
        print("No logs found.")


def show_cmd() -> None:
    if not LOG_PATH.exists():
        print("No logs found.")
        return

    data = LOG_PATH.read_text().strip()
    if not data:
        print("No logs found.")
    else:
        print(data)


def run(args: List[str]) -> None:

    if not args:
        print("Usage: logs <clear|show>")
        return

    cmd = args[0]

    if cmd == "clear":
        clear_cmd()
    elif cmd == "show":
        show_cmd()
    else:
        print(f"Unknown subcommand: {cmd}")
        print("Usage: logs <clear|show>")