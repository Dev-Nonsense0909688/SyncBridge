import time
from sync_bridge import SyncBridge


def test_set_get():
    sb = SyncBridge()

    val = sb.bind("x")
    
    val.set(123)
    test_val = val.get()

    assert val == 123


def test_overwrite():
    sb = SyncBridge()

    sb.set("x", 1)
    sb.set("x", 2)

    assert sb.get("x") == 2


def test_multiple_keys():
    sb = SyncBridge()

    sb.set("a", "hello")
    sb.set("b", 42)

    assert sb.get("a") == "hello"
    assert sb.get("b") == 42
    