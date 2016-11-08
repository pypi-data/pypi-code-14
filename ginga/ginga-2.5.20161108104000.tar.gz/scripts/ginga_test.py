from PySide.QtGui import QApplication

import traceback

app = QApplication([''])

from ginga.qtw.ImageViewCanvasQt import ImageViewCanvas
from ginga.BaseImage import BaseImage
from ginga.misc import log, Bunch

import numpy as np
from glue.core import Data, Subset


class LazyArray(object):

    def __init__(self, subset):
        self._subset = subset

    @property
    def shape(self):
        return self._subset.data.shape

    @property
    def size(self):
        self._subset.data.size

    def __getitem__(self, *args):
        return self._subset.to_mask(args)


class SubsetImage(BaseImage):

    def __init__(self, subset, **kwargs):
        super(SubsetImage, self).__init__(**kwargs)
        self._subset = subset

    def forbidden(self):
        raise ValueError("Forbidden")

    get_data = forbidden
    _get_data = forbidden
    copy_data = forbidden
    set_data = forbidden
    get_array = forbidden
    transfer = forbidden    

    @property
    def shape(self):
        return self._subset.data.shape

    def _get_fast_data(self):
        view = (slice(None, None, 10), slice(None, None, 10))
        return self._view(view)

    def _slice(self, view):
        return self._subset.to_mask(view)

    def _set_minmax(self):
        self.minval = 0
        self.maxval = 1
        self.minval_noinf = self.minval
        self.maxval_noinf = self.maxval
        

# this should make a circular mask
y, x = np.mgrid[-500:500, -500:500]
r = np.hypot(x, y)

d = Data(x=x, y=y, r=r, label='data')

s = d.new_subset()
s.subset_state = d.id['r'] < 30

img = SubsetImage(s)
#img = BaseImage(LazyArray(s))

logger = log.get_logger(name='ginga', log_stderr=True)
canvas = ImageViewCanvas(logger, render='widget')
canvas.set_follow_focus(False)

bindings = canvas.get_bindings()
bindings.enable_all(True)
canvas.enable_draw(False)
canvas.enable_autozoom('off')
canvas.set_zoom_algorithm('rate')
canvas.set_zoomrate(1.4)
canvas.enable_autocuts('off')

canvas.set_image(img)

w = canvas.get_widget()
w.show()
w.raise_()


app.exec_()
