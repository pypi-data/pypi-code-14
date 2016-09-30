'''
Implements the lazy function decorator
'''
from couchpotato.very.lazy import Lazy as LazyStandin

def lazy(func):
    '''
    lazy decorator. Defers evaluation of the function until the value is used.
    '''
    def new_function(*args, **kwargs):
        '''
        Internal decorator function.
        '''
        return LazyStandin(func, args, kwargs)
    new_function.__name__ = func.__name__
    new_function.__doc__ = func.__doc__
    return new_function
