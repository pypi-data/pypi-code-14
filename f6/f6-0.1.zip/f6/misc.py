import socket
import threading
import sys
import os
import time
import math

class timeit(object):

    def __init__(self, name='', output=True, ms=False):
        self.name = name
        self.output = output
        self.beg = 0
        self.end = 0
        self.elapsed = 0
        self.ms = ms

    def __enter__(self):
        self.beg = time.clock()
        return self

    def __exit__(self, *_):
        self.elapsed = time.clock() - self.beg
        if self.output:
            prefix = '{} executed'.format(self.name)
            if self.ms:
                elapsed = '{:.2f}ms'.format(self.elapsed * 1000)
            else:
                elapsed = '{:.6f}s'.format(self.elapsed)
            s = ' '.join([prefix, elapsed]) if self.name else elapsed
            sys.stdout.write(s + '\n')

def send(data, ip='127.0.0.1', port=6560):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(data)
    s.close()

def loc(dir='.',
        includes=None,
        excludes=lambda path, fname: fname == 't.py'):
    if includes is None:
        def includes(path, fname):
            return any(fname.endswith('.' + ext) for ext in (
                'py',
                'c', 'h', 'cpp', #'hpp', 'cc',
                'js',
                'rb',
                'java',
            ))
    n_lines = 0
    for path, dirs, fnames in os.walk(dir):
        for fname in fnames:
            if not excludes(path, fname) and includes(path, fname):
                n_lines += len(open(os.path.join(path, fname)).readlines())
    return n_lines

class bunch(dict):

    def __init__(self, **kwargs):
        super(bunch, self).__init__(kwargs)
        self.__dict__.update(kwargs)

    '''
    >>> b = bunch()
    >>> b.foo = 3
    >>> b
    bunch({'foo': 3})
    '''

identity = lambda e: e

def put(*args):
    try:
        fmt = args[0]
    except IndexError:
        s = ''
    else:
        if (isinstance(fmt, str) or isinstance(fmt, unicode)) and \
                '{' in fmt:
            s = fmt.format(*args[1:])
        else:
            s = ' '.join(map(str, args))
    sys.stdout.write(s + '\n')

def thread(f):
    threading.Thread(target=f).start()
    return f

def files(path):
    for base, dirs, fnames in os.walk(path):
        for fname in fnames:
            yield os.path.join(base, fname)

def human_size(b=0, k=0, m=0, g=0, t=0):
    names = ('B', 'KB', 'MB', 'GB', 'TB')
    factor = 1024
    factors = {}
    cvt_factor = 1
    for name in names:
        factors[name] = cvt_factor
        cvt_factor *= factor
    total_bytes = (
        t * factors['TB']
        + g * factors['GB']
        + m * factors['MB']
        + k * factors['KB']
        + b * factors['B']
    )
    cvted = {name: total_bytes / float(factors[name]) for name in names}
    for name in reversed(names):
        value = cvted[name]
        if math.floor(value) > 0:
            break
    int_value = int(round(value))
    error = abs(value - int_value)
    return '{:.2f}{}'.format(value, name)

if __name__ == '__main__':
    print human_size(m=200, k=980)
