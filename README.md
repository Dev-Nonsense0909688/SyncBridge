# SyncBridge

Direct memory-to-memory synchronization across machines.

SyncBridge lets multiple computers behave like they share the same memory. It uses memory-mapped files (mmap) for local speed and UDP to sync data between systems.

---

## Overview

Most systems communicate using request/response APIs, which add delay and overhead.
SyncBridge avoids that by keeping a shared memory region and syncing it in the background.

* Local processes read and write directly to memory
* A daemon syncs changes to other machines
* Works across Windows and Linux
* Can be used from different languages (Python, C++, Rust)



## How It Works

SyncBridge creates a fixed-size memory block and divides it into predefined sections.
Each variable is assigned a fixed offset and type.

A background process monitors changes and sends updates to peers using UDP.

## Config Sample 

```json
{
    "settings":{
        "name": "sync-bridge",
        "max-space": 2048,
        "port": 9899
    },
    "peers":{
        "192.168.0.211": 9899
    },
    "cmd_settings": {
        "linux": "python3",
        "windows": "py"
    }
}
```

## Example Usage (Python: Vision)

```python
from sync_bridge import SyncBridge

sb = SyncBridge()

status = sb.bind("cloud_status")

status.set("TERMINATE")

print(status.get())
```



## Features

* Memory-mapped storage for fast local access
* Binary encoding using `struct`
* UDP-based synchronization between nodes
* Basic thread safety in memory handling
* Supports two popular platforms: windows, linux
* Supports data types: `int`, `bool`, `float`, `str`



## Installation

```
git clone https://github.com/Dev-Nonsense0909688/SyncBridge.git
cd SyncBridge
pip install -e .
```


## Usage

Start the system:

```bash
sb daemon up/start
```

Stop it:

```bash
sb daemon down/stop
```

Check status:

```bash
sb daemon status
```

Set a value:

```bash
sb set threat_level 99
```

Get a value

```bash
sb get threat_level ## Expected Output: 99
```



## Project Structure

```
src/
 ├── core/
 ├── daemon/
 ├── networking/
 ├── commands/
 ├── utils/
 ├── cli.py
 └── __main__.py
```


## Limitations

* No distributed locking yet
* Not production ready
* Tested only with 2 nodes. 


## Roadmap
* [x] V0.1: Implementation of the CLI with working Memory Allocator and UDP Sync
* [ ] V1: Python implementation with more reliable UDP sync
* [ ] V2: C++ and Rust clients


## License

MIT
