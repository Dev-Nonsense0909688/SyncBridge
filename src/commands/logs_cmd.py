from src.utils.config import BASE_DIR, PLATFORM
import os

LOGS_FOLDER = BASE_DIR.parent

def clear_cmd(args):
    path = os.path.join(LOGS_FOLDER, f"sync-{PLATFORM}.log")
    if os.path.exists(path):
        open(path,"w").write("")
        print("Logs cleared")
    else:
        print("No logs found")

def show_cmd(args):
    path = os.path.join(LOGS_FOLDER, f"sync-{PLATFORM}.log")
    if os.path.exists(path):
        data = open(path).read()
        if data == "":
            print("No logs found")
        else:
            print(data)
    else:
        print("No logs found")