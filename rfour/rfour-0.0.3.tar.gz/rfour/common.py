import arrow

__all__ = [
    'datetime_f'
]

def datetime_f():
    return str(arrow.utcnow().float_timestamp)
