from util.constants import SIZE

def is_ok():
    if SIZE < 1024:
        return False
    return True
