'''This is mma2py.py module, and this module provides Depth, Faltten, Map, MapThread, Nest
 functions. It\'s a link from Mathematica to Python, and with it, you could code with Python
  like Mathematica functionally '''
def Depth(l):
    '''return the Depth of a list'''
    return max(map(Depth, l)) + 1 if isinstance(l, list) else 0

def Flatten(l, n):
    '''Flatten a list with n level, n = "Infinity" is flatten to 1 height.'''
    def flatten(l):
        for el in l:
            if isinstance(el, list):
                for sub in el:
                    yield sub
            else:
            	yield el
    return Flatten(l, Depth(l)) if n == 'Infinity' else Nest(lambda x: list(flatten(x)), l, n)

def Map(f, expr, levelspace = 1):
    '''Map a function on a list in levelspace'''
    return list(map(f, expr)) if levelspace == 1 else list(map(lambda x: Map(f, x, levelspace - 1), expr))

def MapThread(f, expr, levelspace = 1):
    '''MapThread a function on a list in levelspace'''
    temp = [[el[i] for el in expr] for i in range(len(expr[0]))]
    return list(map(f, temp)) if levelspace == 1 else list(map(lambda x: MapThread(f, x, levelspace - 1), temp))

def Nest(f, init, time):
    '''f function on init with time times'''
    return f(init) if time == 1 else f(Nest(f, init, time - 1))