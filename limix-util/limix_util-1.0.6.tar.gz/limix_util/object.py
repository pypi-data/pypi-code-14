def fullname(o):
    """Object's full name.
    :param object o: object.
    :returns: full name.
    """
    return o.__class__.__module__ + "." + o.__class__.__name__
