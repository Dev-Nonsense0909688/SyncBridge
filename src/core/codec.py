import struct

def encode(value):
    if isinstance(value, bool):
        return struct.pack("<?", value), "bool"
    elif isinstance(value, int):
        return struct.pack("<q", value), "int"
    elif isinstance(value, float):
        return struct.pack("<d", value), "float"
    elif isinstance(value, str):
        b = value.encode()
        return struct.pack(f"<I{len(b)}s", len(b), b), "str"
    else:
        raise ValueError("Unsupported type")


def decode(data, dtype):
    if dtype == "bool":
        return struct.unpack("<?", data[:1])[0]
    elif dtype == "int":
        return struct.unpack("<q", data[:8])[0]
    elif dtype == "float":
        return struct.unpack("<d", data[:8])[0]
    elif dtype == "str":
        l = struct.unpack("<I", data[:4])[0]
        return data[4:4+l].decode()