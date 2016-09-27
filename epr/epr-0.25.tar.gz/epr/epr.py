from termcolor import colored
import json

def epr(i, color=None, attrs=[]):
    if isinstance(i, str):
        print(colored(i, color, attrs=attrs))
    else:
        print(colored(json.dumps(i, sort_keys=True, indent=4), color, attrs=attrs))
    return i
