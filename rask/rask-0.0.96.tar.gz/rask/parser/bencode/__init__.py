from bencode import bdecode as decode, bencode
from bencode.BTL import BTFailure
import types

__all__ = [
    'BTFailure',
    'decode',
    'encode'
]

def u_dict(_):
    f = {}
    
    for k,v in _.items():
        f[str(k)] = u_decoder(v)

    return f

def u_list(_):
    return [u_decoder(v) for v in _]

def u_null(_):
    return _

def u_unicode(_):
    return str(_)

def u_decoder(_):
    return {
        "<type 'dict'>":u_dict,
        "<type 'list'>":u_list,
        "<type 'unicode'>":u_unicode
    }.get(str(type(_)),u_null)(_)

        
def encode(_):
    return bencode(u_dict(_))
