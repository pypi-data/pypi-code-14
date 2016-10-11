from os.path import getmtime
import datetime


def match(path, age=0):
    if age < 0:
        age = 0

    if not __older_than(path, age):
        return False

    return True

def __older_than(path, age):
    lmod = datetime.datetime.fromtimestamp(getmtime(path))
    fage = (datetime.datetime.now()-lmod).days
    #print("(age: {0})\n".format(fage))
    return fage > age