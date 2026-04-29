import argparse
import sys
from src.utils.config import BASE_DIR

import os
logs_folder = os.path.join(BASE_DIR.parent,"logs")
os.makedirs(logs_folder, exist_ok=True)

from src.commands.set_cmd import cmd_set
from src.commands.get_cmd import cmd_get
from src.commands.list_cmd import cmd_list
from src.commands.del_cmd import cmd_del
from src.commands.daemon_cmd import cmd_up, cmd_down
from src.commands.logs_cmd import clear_cmd, show_cmd

# ---------------- DAEMON ----------------
def cmd_status(args):
    print("Blehhhh >:3")


# ---------------- MAIN ----------------
def main():
    parser = argparse.ArgumentParser(
        prog="sb",
        description="⚡ SyncBridge CLI — distributed memory like it's local",
    )

    parser.add_argument("-v", "--version", action="version", version="sb 0.1.0")

    sub = parser.add_subparsers(dest="cmd", metavar="<command>")

    # ---------- SET ----------
    p_set = sub.add_parser("set", help="Set a key-value pair")
    p_set.add_argument("key")
    p_set.add_argument("value")
    p_set.set_defaults(func=cmd_set)

    # ---------- GET ----------
    p_get = sub.add_parser("get", help="Get value by key")
    p_get.add_argument("key")
    p_get.set_defaults(func=cmd_get)

    # ---------- LIST ----------
    p_list = sub.add_parser("list", help="List all keys")
    p_list.set_defaults(func=cmd_list)

    # ---------- DELETE ----------
    p_del = sub.add_parser("del", help="Delete a key")
    p_del.add_argument("key")
    p_del.set_defaults(func=cmd_del)

    # ---------- DAEMON ----------
    s_daemon = sub.add_parser("daemon", help="Manage background daemon")

    daemon_sub = s_daemon.add_subparsers(dest="action")

    d_start = daemon_sub.add_parser("start", help="Start daemon")
    d_start.set_defaults(func=cmd_up)

    d_stop = daemon_sub.add_parser("stop", help="Stop daemon")
    d_stop.set_defaults(func=cmd_down)

    d_status = daemon_sub.add_parser("status", help="Check daemon status")
    d_status.set_defaults(func=cmd_status)


    # logs command
    s_logs = sub.add_parser("logs", help="Logs Bruhhh")
    logs_sub = s_logs.add_subparsers(dest="sub", required=True)

    # clear logs
    p_clear = logs_sub.add_parser("clear", help="Clear logs")
    p_clear.set_defaults(func=clear_cmd)

    # show logs
    p_show = logs_sub.add_parser("show", help="Show logs")
    p_show.set_defaults(func=show_cmd)
     

    # ---------- PARSE ----------
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
