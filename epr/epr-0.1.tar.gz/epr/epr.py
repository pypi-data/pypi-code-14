from termcolor import colored
import json

def epr(i, color='black', attrs=[]):
    if isinstance(i, str):
        print(colored(i, color, attrs=attrs))
    else:
        print(colored(json.dumps(i), color, attrs=attrs))
    return i
