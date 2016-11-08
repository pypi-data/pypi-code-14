from ginga.canvas.types.layer import DrawingCanvas

from vispy import scene

class VispyDrawingCanvas(DrawingCanvas):

    def __init__(self, bg, **kwdargs):
        self.v_canvas = scene.SceneCanvas(keys='interactive',
                                          bgcolor=bg)
        super(VispyDrawingCanvas, self).__init__(**kwdargs)

    def update_canvas(self, whence=3):
        self.v_canvas.update()

        super(VispyDrawingCanvas, self).update_canvas(whence=whence)
