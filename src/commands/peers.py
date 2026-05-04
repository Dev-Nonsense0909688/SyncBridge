from src.util.constants import PEERS
from src.util.check_daemon import is_running

def run(args):
    if not is_running(): 
        print("Start the service using command `serve`")
        return
        
    for p in PEERS:
        print(p)