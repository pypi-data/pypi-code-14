"""
Defines all Exceptions used by the GeoPlot package
"""


class GeoPlotError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class MapError(GeoPlotError):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class FieldError(GeoPlotError):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
