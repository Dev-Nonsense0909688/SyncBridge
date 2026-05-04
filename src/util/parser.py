import ast


def parse(val):
    try:
        if val == "true": return True
        elif val == "false": return False
        
        return ast.literal_eval(val)
    except:
        return val
