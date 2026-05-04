import win32event

class Lock:
    def __init__(self, name="Global\\sync_lock"):
        self.handle = win32event.CreateMutex(None, False, name)

    def acquire(self):
        win32event.WaitForSingleObject(self.handle, win32event.INFINITE)

    def release(self):
        win32event.ReleaseMutex(self.handle)

    def __enter__(self):
        self.acquire()

    def __exit__(self, *args):
        self.release()