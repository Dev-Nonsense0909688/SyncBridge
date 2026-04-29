from src.core.registry import VariableRegistry

def cmd_list(args):
    reg = VariableRegistry()
    data = reg.all_keys()

    if not data:
        print("No keys")
        return

    for k, v in data.items():
        print(f"{k} -> {v}")