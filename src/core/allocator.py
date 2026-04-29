from src.utils.config import SIZE, HEADER_SIZE
import mmap
import sys
import struct
import os

class MemoryAllocator:
    def __init__(self, name="sync_bridge"):
        self.name = name
        self.platform = sys.platform
        self.mm = self._open()
        self._init()
        

    def _open(self):
        if self.platform == "win32":
            return mmap.mmap(-1, SIZE, tagname=self.name)

        elif self.platform.startswith("linux"):
            path = f"/dev/shm/{self.name}"
            fd = os.open(path, os.O_CREAT | os.O_RDWR)

            if os.path.getsize(path) < SIZE:
                os.ftruncate(fd, SIZE)

            mm = mmap.mmap(fd, SIZE)
            os.close(fd)
            return mm

        else:
            raise NotImplementedError("Unsupported OS")

    def _init(self):
        if self._read_u32(0) == 0:
            self._write_u32(0, 4)
            self._write_block(4, SIZE - 4, 0, 0)

    def _read_u32(self, o):
        return struct.unpack("<I", self.mm[o:o+4])[0]

    def _write_u32(self, o, v):
        self.mm[o:o+4] = struct.pack("<I", v)

    def _write_block(self, ptr, size, used, nxt):
        self._write_u32(ptr, size)
        self.mm[ptr+4:ptr+5] = bytes([used])
        self._write_u32(ptr+5, nxt)

    def _read_block(self, ptr):
        return (
            self._read_u32(ptr),
            self.mm[ptr+4],
            self._read_u32(ptr+5)
        )

    def alloc(self, size):
        if size <= 0 or size > SIZE:
            raise ValueError("Invalid allocation size")
        
        ptr = 4

        while ptr:
            bsize, used, nxt = self._read_block(ptr)

            if not used and bsize >= size + HEADER_SIZE:
                new_ptr = ptr + HEADER_SIZE + size
                remaining = bsize - size - HEADER_SIZE

                self._write_block(new_ptr, remaining, 0, nxt)
                self._write_block(ptr, size, 1, new_ptr)

                return ptr + HEADER_SIZE

            ptr = nxt

        raise MemoryError("Out of memory")

    def write(self, data_ptr, data: bytes):
        ptr = data_ptr - HEADER_SIZE
        size, used, nxt = self._read_block(ptr)

        if len(data) <= size:
            self.mm[data_ptr:data_ptr+len(data)] = data
            return data_ptr

        new_ptr = self.alloc(len(data))
        self.mm[new_ptr:new_ptr+len(data)] = data
        self.free(data_ptr)
        return new_ptr

    def read(self, data_ptr, size):
        return self.mm[data_ptr:data_ptr+size]

    def free(self, data_ptr):
        ptr = data_ptr - HEADER_SIZE
        size, _, nxt = self._read_block(ptr)
        self._write_block(ptr, size, 0, nxt)
        self._coalesce()

    def _coalesce(self):
        ptr = 4
        while ptr:
            size, used, nxt = self._read_block(ptr)

            if nxt:
                nsize, nused, nnxt = self._read_block(nxt)
                if not used and not nused:
                    self._write_block(ptr, size + nsize + HEADER_SIZE, 0, nnxt)
                    continue

            ptr = nxt
