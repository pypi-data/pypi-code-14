from .simplad_bundle import SimpladBundle

def pipe(first, *args):
    return SimpladBundle().unit(first).pipe(args)
