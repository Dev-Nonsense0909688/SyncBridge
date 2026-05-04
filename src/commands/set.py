from core import Memory, VariableRegistry
from core.codec import encode
from util.constants import REGISTRY_FILE

from util.check_daemon import is_running
def run(args):
    if not is_running(): 
        print("Start the service using command `serve`")
        return
        
    key = args[0]
    val = args[1]

    mem = Memory()
    reg = VariableRegistry(REGISTRY_FILE)
    
    data : dict = reg.get_key(key)
    
    if not data:
        ptr = mem.alloc()
        mem.write(ptr, encode(val)[0])
        reg.set_key(key, {"index": ptr, "type": encode(val)[1]})
        return
    
    ptr = data.get("index")
    mem.write(ptr, encode(val)[0])
    reg.set_key(key, {"index": ptr, "type": encode(val)[1]})
    
    
    

    
    