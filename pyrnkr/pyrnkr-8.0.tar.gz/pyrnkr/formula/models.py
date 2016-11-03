class Trace(object):
    TYPE_HISTOGRAM = 'histogram'

    def __init__(self, title, x, trace_type):
        if not isinstance(x, list):
            raise Exception('x parameter is not an instance of list')

        self._title = title
        self._x = x
        self._trace_type = trace_type

    def to_python(self):
        return {
            'title': self._title,
            'x': self._x,
            'type': self._trace_type
        }


class Layout(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def to_python(self):
        return self
