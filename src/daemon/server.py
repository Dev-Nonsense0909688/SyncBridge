import mmap
import time
import logging

from src.util.constants import SIZE

NAME = "Local\\sync_bridge"

# ---------- LOGGING ----------
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("memory")


def server():
    logger.info("Memory Server Booting...")
    logger.info(f"Allocating {SIZE} bytes")
    logger.info(f"Name: {NAME}")

    mm = None

    try:
        mm = mmap.mmap(-1, SIZE, tagname=NAME)
        logger.info("Memory mapped")

        mm[:] = b"\x00" * SIZE
        logger.info("Memory cleared")

        mm[-1] = 1
        logger.info("Heartbeat set")

        logger.info("Running...")

        uptime = 0
        while True:
            time.sleep(1)
            uptime += 1

            if uptime % 5 == 0:
                logger.debug(f"Uptime: {uptime}s")

    except KeyboardInterrupt:
        logger.info("Stopping...")

    except Exception as e:
        logger.error(f"Error: {e}")

    finally:
        if mm:
            mm.close()
        logger.info("Closed")


if __name__ == "__main__":
    server()
