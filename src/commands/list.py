from src.core import VariableRegistry
from src.util.constants import REGISTRY_FILE
from src.util.check_daemon import is_running

def run(args):
    if not is_running(): 
        print("Start the service using command `serve`")
        return
        
    reg = VariableRegistry(REGISTRY_FILE)
    for v, k in reg.data.items():
        print(v, k)