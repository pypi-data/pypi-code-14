from __future__ import absolute_import, print_function, unicode_literals


def to_str(func, args, kwargs, length=None):
    """Convert the function call into a string representation.

    :param func: the function to convert
    :type func: callable
    :param args: the function arguments
    :type args: list
    :param kwargs: the function keyword arguments
    :type kwargs: dict
    :param length: the maximum length of the string before trimming
    :type length: int
    :return: the string form of the function call
    :rtype: str
    """
    arguments = list(map(repr, args))
    arguments.extend(k + '=' + repr(v) for k, v in kwargs.items())
    representation = ', '.join(arguments)

    if length is not None and len(representation) > length:
        representation = representation[:length] + '...'

    return '{function}({arguments})'.format(
        function=func.__name__,
        arguments=representation
    )
