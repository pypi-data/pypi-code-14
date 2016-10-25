"""A collection of functional-programming primitives, loosely modeled after
ramda.js (http://ramdajs.com/).

Basic philosophy for all functions in this module:

- Prefer immutable data structures; particularly, prefer tuples over lists.
- Pure functions (none of the functions in this module have any observable side
  effects, but some use in-place mutations for efficiency or practicality).
- Composability: function arguments are ordered to maximize composability, that
  is, the most variable argument comes last.
- Total functions: functions should accept *any* value, at least for their
  documented parameter types, and should never raise exceptions for arguments
  of the correct types. This means that, for example, the head() function will
  return None rather than raise an exception when you pass an empty list, and
  likewise, the prop() function will return None when you try to get a
  nonexistent property from a dict.

Other design principles:

- Strings and bytestrings should behave like scalars, not lists-of-characters /
  list-of-bytes, in most situations.
- While our functions are pure, we do not take extra measures to avoid
  manipulation of data we handle from outside. If you pass in a mutable data
  structure, we will not manipulate it in place, but we may return the original
  data structure when no modifications are required, and we may return
  references to parts of it rather than copying said parts. For example, the
  prop() function will return a reference to the object stored at a particular
  key, not a deep copy; and the identity() function will never attempt to copy
  its argument.
"""

def fmap(f, d):
    """ A generalized "map()", similar to the "fmap" function in Haskell.
    Applies the function "f" in the functor "d". For the purposes of this
    function, the following things are considered functors:
    - Dictionary-like objects (anything that has an .items() function); here,
      "f" is applied to the values, keeping the keys and key-value relationships
      intact.
    - Iterables; "f" is applied to all the values, ordering is kept intact.
    - Functions; returns a new function that passes its arguments to "d" and
      then applied "f" to the return value.
    - Anything else is considered an option, "f" is applied if "d" is not None.
    """
    if hasattr(d, "items") and callable(d.items):
        return dict( ( (k, f(v)) for k, v in d.items() ) )
    elif hasattr(d, "__iter__"):
        return map(f, d)
    elif callable(d):
        def wrapped(*args, **kwargs):
            retval = d(*args, **kwargs)
            if retval is None:
                return None
            else:
                return f(retval)
        return wrapped
    elif d is None:
        return None
    else:
        return f(d)

def assoc(key, val, obj=None):
    """Add ("associate") "val" as "key" to "obj". "obj" should be a
    dictionary-like object; if it is None, then a new empty dict will be
    created. The return value will always be a dict, casting the original
    argument as needed.
    """
    new_obj = {} if obj is None else dict(obj)
    new_obj[key] = val
    return new_obj

def assocs(keyvals, obj=None):
    """Associate multiple key/value pairs into "obj". "keyvals" should be a
    list-like collection of pairs (2-tuples or other 2-element list-likes).
    """
    new_obj = obj
    for k,v in keyvals:
        new_obj = assoc(k, v, new_obj)
    return new_obj

def dissoc(key, obj):
    """Remove ("associate") "key" from "obj". "obj" should be a dictionary-like
    object. The return value will always be a dict, casting the original
    argument as needed.
    """
    new_obj = dict(obj)
    new_obj.pop(key)
    return new_obj

def _tuplize(t):
    if type(t) is str or type(t) is bytes:
        return (t,)
    if t is None:
        return ()
    try:
        return tuple(t)
    except TypeError:
        return (t,)

def cons(h, t=None):
    """Prepend a single element to a list-like structure. Always returns a
    tuple.
    """
    return (h,) + _tuplize(t)

def snoc(h, t=None):
    """Append a single element to a list-like structure. Always returns a
    tuple.
    """
    return _tuplize(t) + (h,)

def take(n, t):
    """Take the first "n" elements of list-like "t", or all of "t" if it is
    shorter than "n" elements. Effectively, like t[:n], but always return a
    tuple.
    """
    if n <= 0:
        return ()
    return _tuplize(t)[:n]

def drop(n, t):
    """Take all but the first "n" elements of list-like "t", or an empty tuple
    if "t" is shorter than "n" elements. Effectively, like t[n:], but always
    return a tuple.
    """
    if n <= 0:
        return _tuplize(t)
    return _tuplize(t)[n:]

def drop_end(n, t):
    """Like drop(), but remove elements from the end.
    """
    if n <= 0:
        return _tuplize(t)
    return _tuplize(t)[:-n]

def take_end(n, t):
    """Like drop(), but take elements from the end.
    """
    if n <= 0:
        return ()
    return _tuplize(t)[-n:]

def nth(n, t=None):
    """Get the nth element (0-based) from a list-like, or None if the list has
    "n" or fewer elements.
    """
    if t is None:
        return None
    n = int(n)
    if n < 0:
        return None
    try:
        return t[n]
    except IndexError:
        return None

def head(t):
    """Get the first element from a list-like, or None if it's empty.
    """
    return nth(0, t)

def last(t):
    """Get the last element from a list-like, or None if it's empty.
    """
    if t is None:
        return None
    return nth(len(t) - 1, t)

def tail(t):
    """Get all but the first elements from a list-like, as a tuple.
    """
    return drop(1, t)

def fold(func, items, initial=None):
    """Left-leaning fold. 
    """
    accum = initial
    for item in _tuplize(items):
        accum = func(accum, item)
    return accum

def concat(items):
    """List concatenation (actually tuples).
    Takes a list-like of list-likes, turns each element into a tuple, and
    concatenates all these tuples into one. Any element that is not a list-like
    will be converted into a 1-element tuple, unless it is None, in which case
    it is converted into an empty tuple.
    """
    return fold(lambda x, y: _tuplize(x) + _tuplize(y), items, ())

def flatten(items):
    """Recursively flatten a nested data structure into a flat tuple of
    elements. Data structures that are considered flattenable are:
    - List-like collections except bytestrings and strings: lists, sets,
      tuples, and anything else that has an __iter__() method
    - Dictionary-like collections: dicts, and anything else that has a values()
      method.
    - None (which is treated as an empty list)
    Anything else is considered a scalar value and gets added to the flattened
    list unchanged.
    """
    # special case for None:
    if items is None:
        return ()
    # special case for strings and bytestrings:
    if isinstance(items, str):
        return (items,)
    if isinstance(items, bytes):
        return (items,)
    # if it's a dict-like, use just the values:
    if hasattr(items, 'values') and callable(items.values):
        return flatten(items.values())
    # if it's iterable, turn it into a flat tuple:
    if hasattr(items, '__iter__'):
        return tuple(concat(map(flatten, items)))
    # if it's neither of the above, assume it's scalar, wrap it in a 1-tuple.
    return (items,)

def prop(p, item):
    """Get property "p" from "item", or None if it doesn't exist.
    """
    return prop_lens(p).get(item)

def path(p, item):
    """Given a list-like "p", interpret each of its elements as a property and
    follow the resulting path recursively like "prop()" does. Any failing
    property lookup along the way short-circuits the lookup and returns None.
    """
    return path_lens(p).get(item)

def assoc_path(p, value, item):
    """Associate a "value" into "item" along a "path". The semantics for the
    "path" are the same as those for "path()", but rather than getting the
    value at that position, create a new data structure with the value at that
    position replaced.
    """
    return path_lens(p).set(value, item)

def identity(x, *args, **kwargs):
    """The identity function: return the first argument unchanged, ignore all
    other arguments.
    """
    return x

def compose(f1, f2):
    """Function composition, in mathematical order (outer-first).
    compose(f, g)(x) is equivalent to f(g(x)).
    """
    def f(*args, **kwargs):
        return f1(f2(*args, **kwargs))
    return f

def rcompose(f1, f2):
    """Function composition, in pipeline order (inner-first).
    rcompose(f, g)(x) is equivalent to g(f(x)).
    """
    return compose(f2, f1)

def chain(*fns):
    """Function composition generalized into a variadic function.
    The following equivalencies hold:

    chain() === identity
    chain(f) === f
    chain(f, g) === compose(f, g)
    chain(f, g, h) === compose(f, compose(g, h))
    """
    if len(fns) == 0:
        return identity
    return fold(compose, tail(fns), head(fns))

def dictmap(f, item):
    """Specialized map() / fmap() for dictionaries. Maps over the values of a
    dictionary-like object, retaining keys and key/value relationships.

    For dictionary-like objects, equivalent to fmap(); for anything else, it
    will however raise a TypeError.
    """
    return dict((k, f(v)) for k, v in item.items())

def cat_maybes(items):
    """Specialized filter(), discarding all None's
    """
    return tuple((item for item in items if item is not None))

class Lens(object):
    """A Lens abstracts over a getter/setter pair and represents a "view" on
    a data object.

    Lens Law:

    lens.get(lens.set(value, subject)) == value

    Informally: setting the target of a lens produces an object for which
    getting the target of the same lens will return the value passed to the
    setter.

    Even more informally: lenses behave like properties, lens.get() being the
    analog of dict.get(), and lens.put() the analog of dict.__setitem__().

    Lenses are composable: see the compose_lens() function for a primitive
    lens combinator.
    """
    def __init__(self, getter, setter):
        self.getter = getter
        self.setter = setter

    def get(self, subject):
        """Apply the lens' getter to the subject.
        """
        return self.getter(subject)

    def set(self, value, subject):
        """Apply the lens' setter to the subject.
        """
        return self.setter(value, subject)

    def over(self, f, subject):
        """Modify the target of the lens by applying the given function "f" to it.
        """
        value = self.get(subject)
        if value is None:
            return subject
        return self.set(f(value), subject)

def prop_lens(prop_name):
    """Create a Lens that drills down into a dict-like object's named property.
    """
    def getter(subject):
        if subject is None:
            return None
        return subject.get(prop_name)

    def setter(value, subject):
        if subject is None:
            subject = {}
        return assoc(prop_name, value, subject)

    return Lens(getter, setter)

def path_lens(*path):
    """Create a Lens that follows a path of properties.
    The path can be passed as variable positional args, or as any iterable, or
    any combination thereof, so the following are all equivalent:

    path_lens("foo", "bar", "baz")
    path_lens(["foo", "bar", "baz"])
    path_lens("foo", ["bar", "baz"])
    path_lens(("foo", ("bar", ("baz"))))

    Caveat: some collection types are iterable despite not having a defined
    ordering. Using such types in your path will cause unpredictable behavior,
    because the ordering of path segments cannot be guaranteed. For example:

    path_lens(set(("foo", "bar")))

    ...could produce either foo -> bar or bar -> foo, depending on which
    ordering the set happens to produce. So, uhm, don't do that OK?

    For extra convenience, any of the individual path items can be a lens
    instead of a prop name, which allows you to splice existing lenses into the
    path:

    path_lens("foo", some_lens, "bar")

    This also means that path_lens can act as a generic variadic lens composer
    function, and the following are equivalent:

    path_lens(lens1, lens2, lens3)
    compose_lens(lens1, compose_lens(lens2, lens3))

    """
    path = flatten(path)
    def to_lens(item):
        if isinstance(item, Lens):
            return item
        else:
            return prop_lens(item)
    return fold(
        compose_lens,
        map(to_lens, path),
        identity_lens())

def compose_lens(left, right):
    """Compose lenses outer-to-inner.
    The following are equivalent:
        get(compose_lens(left, right), subject) == get(left, get(right, subject))
    """
    def getter(subject):
        return right.get(left.get(subject))

    def setter(value, subject):
        inner = left.get(subject) or {}
        new_inner = right.set(value, inner)
        return left.set(new_inner, subject)

    return Lens(getter, setter)

def identity_lens():
    """Create a no-op lens that operates on the subject itself. Note, however,
    that .set() is still pure, meaning that it will not modify the subject;
    instead, it will just return the value passed to it and not touch the
    subject at all.
    """
    def getter(subject):
        return subject
    def setter(value, subject):
        return value
    return Lens(getter, setter)
