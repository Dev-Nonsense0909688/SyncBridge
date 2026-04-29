import ast

def parse(val):
    try:
        return ast.literal_eval(val)
    except:
        return val