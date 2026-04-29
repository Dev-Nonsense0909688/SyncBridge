from src.core.registry import VariableRegistry

def run(args):
    reg = VariableRegistry()
    data = reg.all_keys()

    if not data:
        print("No keys")
        return
    i = 1
    for k, v in data.items():
        print(f"{i}. {k}({v['type']})")
        i += 1