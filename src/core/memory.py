import mmap
from src.core.mutex import Lock
from src.util.constants import SIZE as size

SIZE = size - 1
BLOCK_SIZE = 32
TOTAL_BLOCKS = SIZE // BLOCK_SIZE

FREE = b'\x00'
USED = b'\x01'


class Memory:
    def __init__(self):
        self.mm = mmap.mmap(-1, SIZE, "Local\\sync_bridge")
        self.lock = Lock()
        if self.mm[0] != 1:
            self.mm[0] = 1
            self._init_blocks()

    def _init_blocks(self):
        for i in range(TOTAL_BLOCKS):
            offset = i * BLOCK_SIZE
            # 1 byte = free flag (0A = free, 0B = used)
            self.mm[offset:offset+1] = FREE

    def get_free_blocks(self):
        free = []
        for i in range(TOTAL_BLOCKS):
            offset = i * BLOCK_SIZE
            # print(self.mm[0:4], FREE)
            if self.mm[offset:offset+1] == FREE:
                free.append(i)
        return free

    def alloc(self):
        with self.lock:
            for i in range(TOTAL_BLOCKS):
                offset = i * BLOCK_SIZE
                if self.mm[offset:offset+1] == FREE:
                    self.mm[offset:offset+1] = USED
                    return i  # return block index
        return None  # no space

    def free(self, index):
        with self.lock:
            offset = index * BLOCK_SIZE
            self.mm[offset:offset+1] = FREE

    def write(self, index, data: bytes):
        if len(data) > BLOCK_SIZE - 5:
            raise ValueError("Too big")

        with self.lock:
            offset = index * BLOCK_SIZE + 1
            self.mm[offset:offset+4] = len(data).to_bytes(4, "little")
            self.mm[offset+4:offset+4+len(data)] = data

    def read(self, index):
        offset = index * BLOCK_SIZE + 1
        size = int.from_bytes(self.mm[offset:offset+4], "little")
        return self.mm[offset+4:offset+4+size]
