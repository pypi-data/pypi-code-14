def isfloat(value):
    """Tests whether the provided object can be converted to a float."""
    try:
        float(value)
        return True
    except ValueError:
        return False

def isint(value):
    """Tests whether the provided object can be converted to an integer without
    losing information."""
    try:
        return float(value) == int(value)
    except ValueError:
        return False

def isnumber(value):
    """Returns isfloat(value) or isint(value)."""
    return isfloat(value) or isint(value)
