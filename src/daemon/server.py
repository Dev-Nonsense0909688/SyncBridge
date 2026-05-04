import mmap
import time
import sys
from src.util.constants import SIZE

NAME = "Local\\sync_bridge"

def server():
    print("=" * 50)
    print("Memory Server Booting...")
    print(f"[INFO] Allocating {SIZE} bytes in RAM")
    print(f"[INFO] Shared memory name: {NAME}")
    print("=" * 50)

    try:
        # Create shared memory
        mm = mmap.mmap(-1, SIZE, tagname=NAME)
        print("[OK] Memory mapped successfully")

        # Initialize memory
        mm[:] = b"\x00" * SIZE
        print("[OK] Memory zeroed out")

        # Mark server alive flag (last byte)
        mm[len(mm) - 1] = 1
        print("[OK] Heartbeat flag set")

        print("\n[RUNNING] Server is alive. Waiting...\n")

        uptime = 0
        while True:
            time.sleep(1)
            uptime += 1

            # optional debug every 5 sec
            if uptime % 5 == 0:
                flag = mm[len(mm) - 1]
                print(f"[DEBUG] Uptime: {uptime}s | Alive flag: {flag}")

    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Ctrl+C detected")

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        print("[CLEANUP] Closing memory...")
        try:
            mm.close()
        except:
            pass
        print("[EXIT] Server stopped.")

server()