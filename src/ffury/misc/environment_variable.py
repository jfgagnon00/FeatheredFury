import os

def getenv(var_name):
    value = os.getenv(var_name)
    if value is None or value == "":
        raise ValueError(f"{var_name} non definie")
    return value
