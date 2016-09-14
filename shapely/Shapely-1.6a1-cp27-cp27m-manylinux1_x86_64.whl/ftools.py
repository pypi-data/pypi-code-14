# Backport some of functools from Python 2.5 standard library for Shapely 
# on Python 2.4
#
# Python module wrapper for _functools C module
# to allow utilities written in Python to be added
# to the functools module.
# Written by Nick Coghlan <ncoghlan at gmail.com>
# Copyright (C) 2006 Python Software Foundation.
# See C source code for _functools credits/copyright
#
# _functools module written and maintained
# by Hye-Shik Chang <perky@FreeBSD.org>
# with adaptations by Raymond Hettinger <python@rcn.com>
# Copyright (c) 2004, 2005, 2006 Python Software Foundation.
# All rights reserved.

def _partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(
            *(args + fargs), **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc

# update_wrapper() and wraps() are tools to help write
# wrapper functions that can handle naive introspection

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__')
WRAPPER_UPDATES = ('__dict__',)
def _update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper

def _wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return _partial(_update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)

# Use stdlib's functools if available
try:
    from functools import partial, update_wrapper, wraps
    have_functools = 1
except ImportError:
    partial = _partial
    update_wrapper = _update_wrapper
    wraps = _wraps
    have_functools = 0

