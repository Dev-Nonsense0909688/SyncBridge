from src.core.memory import Memory, TOTAL_BLOCKS

from util.check_daemon import is_running
def run(args):
    if not is_running(): 
        print("Start the service using command `serve`")
        return
        
    mem = Memory()
    for i in range(TOTAL_BLOCKS):  
        mem.free(i)