"""Text construction based on str"""


def enumeration(items, link='and'):
    "['a', 'b', 'c'] -> 'a, b and c'"
    if len(items) >= 2:
        return (' %s ' % link).join((', '.join(items[:-1]), items[-1]))
    elif len(items) == 1:
        return items[0]
    else:
        raise ValueError("items=%s" % repr(items))


def n_of(n, of, plural_for_0=False):
    "n_of(3, 'epoch') -> '3 epochs'"
    if n == 0:
        if plural_for_0:
            return "no " + of + 's'
        else:
            return "no " + of
    elif n == 1:
        return "1 " + of
    else:
        return str(n) + ' ' + of + 's'


def named_list(items, name='item'):
    "named_list([1, 2, 3], 'number') -> 'numbers (1, 2, 3)"
    if len(items) == 1:
        return "%s (%r)" % (name, items[0])
    else:
        if name.endswith('y'):
            name = name[:-1] + 'ie'
        return "%ss (%s)" % (name, ', '.join(map(repr, items)))


def plural(noun, n):
    "plural('ant', 1) -> 'ant';  plural('ant', 2) -> 'ants'"
    return noun + 's' if n > 1 else noun
