# -*- coding: utf-8 -*-

"""Access an object's name as a property

Autoname is a data-descriptor, which automatically looks up the
name under which the object on which the descriptor is accessed
is known by.

Import the descriptor using ``from mtoolbox.autoname import Autoname``.

Example:

    >>> class Object(object):
    ...     name = Autoname()
    >>> o = Object()
    >>> o.name
    'o'

By default Autoname will return the outer-most name that was defined
for the object:

    >>> class Object(object):
    ...     name = Autoname()
    >>> def func(anobject):
    ...     return anobject.name
    >>> o = Object()
    >>> func(Object())
    'anobject'
    >>>
    >>> g = o
    >>> g.name
    'o'
    >>> del o
    >>> g.name
    'g'

You can change this behaviour by using the 'first' keyword:

    >>> class Object(object):
    ...     name = Autoname(first=True)
    >>> o = Object()
    >>> o.name
    'o'
    >>> g = o
    >>> g.name
    'g'
    >>> o.name
    'g'

Note:
    Please be aware, that getting the inner-most name, is not what you
    want in most cases:

    >>> class Object(object):
    ...     name = Autoname(first=True)
    ...     def printname(self):
    ...         print(self.name)
    >>> o = Object()
    >>> o.printname()
    self
"""

import doctest
import inspect

class Autoname(object):
    """Create a new Autoname descriptor

    Args:
        initval (str, bool, None): The initial name
        first (bool): Return the first found name of the object (or not)

    Returns:
        Autoname: An Autoname instance
    """

    def __init__(self, initval=True, first=False):
        self.val = None
        self.first = first
        self.__set__(None, initval)

    def __get__(self, theobject, objtype):
        """Return the name of theobject or None

        Returns:
            str or None: the name of the object

        Usage:

            >>> class Object(object):
            ...     name = Autoname(first=True)
            >>> obj = Object()
            >>> obj.name
            'obj'
            >>> obj.name = 'another name'
            >>> obj.name
            'another name'
        """
        if isinstance(self.val, str):
            return self.val
        elif self.val is False or self.val is None:
            return None
        else:
            # If we really didn't find a name, we return None
            thename = None

            # There is at least one frame in the callstack, in which
            # the calling object is a local variable, so we climb up
            # the callstack, to find the name of the object.
            for count, frametuple in enumerate(inspect.stack()):
                # skip the first frame - this is our __get__
                if count == 0:
                    continue

                for name, obj in frametuple[0].f_locals.items():
                    # found a name, but keep searching in order to get
                    # the outer-most name
                    if obj == theobject:
                        thename = name
                        if self.first:
                            return thename

            return thename

    def __set__(self, theobject, val):
        """Set the name of the theobject

        Args:
            theobject (object): The object to which's class
                                the descriptor is attached to

            val (str, bool or None): Sets the name to depending on the type:
                str sets the name to this str.
                False or None sets the name to None.
                True sets the name to automatically lookup.

        Returns:
            None

        Raises:
            TypeError if type(val) is invalid

        Usage:
            >>> class Object(object):
            ...     name = Autoname()
            >>> o = Object()
            >>> o.name = 'k'
            >>> o.name
            'k'
            >>> o.name = True
            >>> o.name
            'o'
            >>> o.name = False
            >>> str(o.name)
            'None'
            >>> o.name = 4
            Traceback (most recent call last):
            ...
            TypeError: Autoname must be set to str, bool, NoneType
        """
        types = (str, bool, type(None))

        if not isinstance(val, types):
            raise TypeError("Autoname must be set to %s" % ", ".join(
                [t.__name__ for t in types]))

        self.val = val

if __name__ == '__main__':
    doctest.testmod()


