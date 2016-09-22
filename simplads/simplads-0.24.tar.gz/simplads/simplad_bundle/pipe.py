from .simplad_bundle import SimpladBundle
from .lift import lift

def pipe(first, *args):
    lifted = [lift(i) for i in args]
    return SimpladBundle().unit(first).pipe(lifted)
