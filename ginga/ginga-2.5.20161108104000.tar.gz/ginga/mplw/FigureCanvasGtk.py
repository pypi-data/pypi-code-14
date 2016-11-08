#
# FigureCanvasGtk.py -- classes for the display of FITS files in
#                             Matplotlib FigureCanvas
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.

import matplotlib
matplotlib.use('GTKCairo')
from  matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo \
     as GtkFigureCanvas

import gtk
import gobject

class FigureCanvas(GtkFigureCanvas):
    """Ultimately, this is a gtk Widget (as well as a FigureCanvas, etc.).
    """
    def __init__(self, fig, parent=None, width=5, height=4, dpi=100):
        GtkFigureCanvas.__init__(self, fig)

        self.viewer = None

        ## # For message drawing
        ## self._msg_timer = 0

        ## # For optomized redrawing
        ## self._defer_timer = 0

        w = self
        w.set_can_focus(True)
        w.connect("configure-event", self.configure_event)
        w.connect("size-request", self.size_request)

    def configure_event(self, widget, event):
        rect = widget.get_allocation()
        x, y, width, height = rect.x, rect.y, rect.width, rect.height

        if self.viewer is not None:
            self.viewer.configure_window(width, height)
        return True

    def size_request(self, widget, requisition):
        """Callback function to request our desired size.
        """
        width, height = 300, 300
        if self.viewer is not None:
            width, height = self.viewer.get_desired_size()

        requisition.width, requisition.height = width, height
        return True

    def set_viewer(self, viewer):
        self.viewer = viewer

        ## self._msg_timer.timeout.connect(viewer.onscreen_message_off)
        ## self._defer_timer.timeout.connect(viewer.delayed_redraw)

    ## def onscreen_message(self, text, delay=None, redraw=True):
    ##     if self._msg_timer:
    ##         try:
    ##             gobject.source_remove(self._msg_timer)
    ##         except:
    ##             pass

    ##     if self.viewer is not None:
    ##         self.viewer.message = text
    ##         if redraw:
    ##             self.viewer.redraw(whence=3)
    ##         if delay:
    ##             ms = int(delay * 1000.0)
    ##             self._msg_timer = gobject.timeout_add(ms,
    ##                                                   self.onscreen_message,
    ##                                                   None)
    ## def reschedule_redraw(self, time_sec):
    ##     try:
    ##         gobject.source_remove(self._defer_timer)
    ##     except:
    ##         pass
    ##     if self.viewer is not None:
    ##         self._defer_timer = gobject.timeout_add(time_ms,
    ##                                                 self.viewer.delayed_redraw)


#END
