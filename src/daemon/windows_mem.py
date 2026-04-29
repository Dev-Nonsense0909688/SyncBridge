import mmap
import time

NAME = "Local\\sync_bridge"
SIZE = 1024 * 1024


def server():
    mm = mmap.mmap(-1, SIZE, tagname=NAME)
    mm[:] = b"\x00" * SIZE

    try:
        while True:
            time.sleep(1)
    except:
        pass

    mm.close()

server()
