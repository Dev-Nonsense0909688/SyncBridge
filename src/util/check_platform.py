import sys

def is_ok():
    platform = sys.platform
    if platform == "win32":
        return True
    else:
        return False