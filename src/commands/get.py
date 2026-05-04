from core import Memory, VariableRegistry
from core.codec import decode
from util.constants import REGISTRY_FILE
from util.check_daemon import is_running
def run(args):
    if not is_running(): 
        print("Start the service using command `serve`")
        return
    
    key = args[0]

    mem = Memory()
    reg = VariableRegistry(REGISTRY_FILE)
    
    data : dict = reg.get_key(key)
    
    if not data:
        print(None)
        return
    
    ptr = data.get("index")
    dtype = data.get("type")
    
    print(decode(mem.read(ptr), dtype))
    
    
    

    
    