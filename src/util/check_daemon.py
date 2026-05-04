import mmap

def is_running():
    mm = mmap.mmap(-1, 2048, "Local\\sync_bridge")
    if mm[len(mm) - 1] == 1: return True
    return False

