import re
import os

SECT=re.compile(r'\[([a-zA-Zа-яА-Я_\? ]+)\]')
__TIME__ = 0
__FILE__ = 'strings.conf'
__TEXT__ = ''
__SEGMENTS__ = {}
AUTORELOAD = True

def reload_text():
    global __TEXT__
    with open(__FILE__, 'r') as fl:
        __TEXT__ = fl.read()
    __TIME__ = os.path.getmtime(__FILE__)
    segmentate_text()

def segmentate_text():
    stace = SECT.split(__TEXT__)[1:]
    for (k,v) in zip(stace[::2], stace[1::2]):
        k = k.strip()
        __SEGMENTS__[k] = []
        for line in v.split('\n'):
            line = line.strip()
            if line:
                __SEGMENTS__[k].append(line)

def get_strings(key, default = []):
    if not __TEXT__ or (AUTORELOAD and os.path.getmtime(__FILE__) > __TIME__):
        reload_text()
    return __SEGMENTS__.get(key, default)
    
def get_string(key, default = ''):
    st = '\n'.join(get_strings(key, []))
    return st or default

def print_into(key, printer=print):
    for x in get_strings(key):
        printer(x)

if __name__ == '__main__':
    reload_text()
    print(__SEGMENTS__)
