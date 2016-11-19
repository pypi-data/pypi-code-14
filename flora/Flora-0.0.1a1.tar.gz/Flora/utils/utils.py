from discord import Permissions
from inspect import isfunction

def create_permissions(**args):
    P = Permissions()
    if len(args) == 0:
        P.general()
        return P
    for k in args:
        k = k.lower().replace(' ', '_')
        try:
            P.__getattribute__(k)()
        except (AttributeError, TypeError):
            pass
    return P

def has_permissions(P: Permissions, **kwargs):
    T = []
    for k,v in kwargs.items():
        try:
            T.append(P.__getattribute__(k) == v)
        except (AttributeError, TypeError):
            pass
    return all(T)
