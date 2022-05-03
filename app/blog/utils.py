import ast

def convertListToString(list: list):
    return str(list)

def convertStringToList(string: str):
    return ast.literal_eval(string)
