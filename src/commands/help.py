import os

def run(args):
    commands = {
        "get": "get <key>        -> Retrieve value from SyncBridge",
        "set": "set <key> <val>  -> Store value in SyncBridge",
        "list": "list             -> List all stored keys",
        "peers": "peers           -> Show connected peers",
        "reset": "reset           -> Clear all data",
        "serve": "serve           -> Start the SyncBridge server",
        "help": "help             -> Show this help menu",
    }

    print("Available Commands:\n")
    for cmd, desc in commands.items():
        print(f"{desc}")