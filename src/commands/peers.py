from typing import List, Tuple
from src.utils.config import PEERS


def format_peers(peers: List[Tuple[str, int]]) -> str:
    if not peers:
        return "No peers configured."

    lines = ["Configured peers:\n"]
    for idx, (host, port) in enumerate(peers, start=1):
        lines.append(f"{idx:>2}. {host}:{port}")
    return "\n".join(lines)


def run(args: List[str]) -> None:

    print(format_peers(PEERS))