import pprint
pp = pprint.PrettyPrinter(indent=4)

def pr(i):
    print(pp.pprint(i))
    return i
