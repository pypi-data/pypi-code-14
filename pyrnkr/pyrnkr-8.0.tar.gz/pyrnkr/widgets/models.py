from pyrnkr.formula.models import Trace, Layout


class Widget(object):
    kind = None
    layout = Layout()

    def __init__(self, title='Blank', subtitle='Blank', dimension='col-md-4',):
        self._title = title
        self._subtitle = subtitle
        self._dimension = dimension

    def to_python(self):
        pass

    def render(self):
        return {
            'title': self._title,
            'subtitle': self._subtitle,
            'dimension': self._dimension,
            'layout': self.layout.to_python(),
            'data': self.to_python(),
            'kind': self.kind
        }


class Tabular(Widget):

    def __init__(self, rows, cols, **kwargs):
        super(Tabular, self).__init__(**kwargs)
        self._rows = rows
        self._cols = cols

    def to_python(self):
        return {
            'rows': self._rows,
            'cols': self._cols
        }


class Histogram(Widget):

    def __init__(self, traces, **kwargs):
        super(Histogram, self).__init__(**kwargs)
        self._traces = traces

    def to_python(self):
        return {
            'traces': [x.to_python() for x in self._traces],
        }


class StackedHistogram(Histogram):
    kind = 'Histogram'

    def __init__(self, traces, **kwargs):
        self.layout = Layout(barmode='stack')
        super(StackedHistogram, self).__init__(traces=traces, **kwargs)


class BasicHistogram(Histogram):
    kind = 'Histogram'

    def __init__(self, trace, **kwargs):
        super(BasicHistogram, self).__init__(traces=[trace], **kwargs)
