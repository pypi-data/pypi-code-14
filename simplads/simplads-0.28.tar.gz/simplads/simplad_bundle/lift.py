from simplads.simplad_monad.namedtuples.simplad_result import SimpladResult

def lift(func):
    return lambda i: SimpladResult(val=func(i), delta_map={})
