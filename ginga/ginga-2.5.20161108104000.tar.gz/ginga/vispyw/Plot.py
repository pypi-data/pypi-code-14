#
# Plot.py -- Plotting widget canvas wrapper.
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
# GUI imports
from vispy import plot as vp

class PlotWidget(Widgets.WidgetBase):

    def __init__(self, plot, width=500, height=500):
        super(PlotWidget, self).__init__()

        fig = vp.Fig(size=(width, height), show=False)
        self.widget = FigureCanvas(plot.get_figure())
        self.widget._resizeEvent = self.widget.resizeEvent
        self.widget.resizeEvent = self.resize_event
        self.plot = plot

    def configure_window(self, wd, ht):
        fig = self.plot.get_figure()
        fig.set_size_inches(float(wd) / fig.dpi, float(ht) / fig.dpi)

    def resize_event(self, event):
        rect = self.widget.geometry()
        x1, y1, x2, y2 = rect.getCoords()
        width = x2 - x1
        height = y2 - y1

        if width > 0 and height > 0:
            self.configure_window(width, height)
            self.widget._resizeEvent(event)

#END
