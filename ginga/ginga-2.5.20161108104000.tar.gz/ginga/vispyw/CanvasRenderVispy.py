#
# CanvasRenderVispy.py -- for rendering into a Vispy canvas
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.

import math

from vispy import app
from vispy import scene
from vispy import visuals
from vispy.visuals.transforms import STTransform
from . import VispyHelp

# force registration of all canvas types
import ginga.canvas.types.all

class RenderContext(object):

    def __init__(self, viewer):
        self.viewer = viewer

        # TODO: encapsulate this drawable
        self.cr = VispyHelp.VispyContext(self.viewer.get_surface())

        self.pen = None
        self.brush = None
        self.font = None

    def set_line_from_shape(self, shape):
        # TODO: support line width and style
        alpha = getattr(shape, 'alpha', 1.0)
        self.pen = self.cr.get_pen(shape.color, alpha=alpha)

    def set_fill_from_shape(self, shape):
        fill = getattr(shape, 'fill', False)
        if fill:
            if hasattr(shape, 'fillcolor') and shape.fillcolor:
                color = shape.fillcolor
            else:
                color = shape.color
            alpha = getattr(shape, 'alpha', 1.0)
            alpha = getattr(shape, 'fillalpha', alpha)
            self.brush = self.cr.get_brush(color, alpha=alpha)
        else:
            self.brush = None

    def set_font_from_shape(self, shape):
        if hasattr(shape, 'font'):
            if hasattr(shape, 'fontsize') and shape.fontsize is not None:
                fontsize = shape.fontsize
            else:
                fontsize = shape.scale_font(self.viewer)
            alpha = getattr(shape, 'alpha', 1.0)
            self.font = self.cr.get_font(shape.font, fontsize, shape.color,
                                         alpha=alpha)
        else:
            self.font = None

    def initialize_from_shape(self, shape, line=True, fill=True, font=True):
        if line:
            self.set_line_from_shape(shape)
        if fill:
            self.set_fill_from_shape(shape)
        if font:
            self.set_font_from_shape(shape)

    def set_line(self, color, alpha=1.0, linewidth=1, style='solid'):
        # TODO: support line width and style
        self.pen = self.cr.get_pen(color, alpha=alpha)

    def set_fill(self, color, alpha=1.0):
        if color is None:
            self.brush = None
        else:
            self.brush = self.cr.get_brush(color, alpha=alpha)

    def set_font(self, fontname, fontsize, color='black', alpha=1.0):
        self.font = self.cr.get_font(fontname, fontsize, color,
                                     alpha=alpha)

    def text_extents(self, text):
        return self.cr.text_extents(text, self.font)

    def get_affine_transform(self, cx, cy, rot_deg):
        x, y = 0, 0          # old center
        nx, ny = cx, cy      # new center
        sx = sy = 1.0        # new scale
        cosine = math.cos(math.radians(rot_deg))
        sine = math.sin(math.radians(rot_deg))
        a = cosine / sx
        b = sine / sx
        c = x - nx*a - ny*b
        d = -sine / sy
        e = cosine / sy
        f = y - nx*d - ny*e
        return (a, b, c, d, e, f)

    ##### DRAWING OPERATIONS #####

    def draw_text(self, cx, cy, text, rot_deg=0.0):
        wd, ht = self.cr.text_extents(text, self.font)

        self.cr.text((cx, cy-ht), text, self.font, self.pen)

    def draw_polygon(self, cpoints):
        self.cr.polygon(cpoints, self.pen, self.brush)

    def draw_circle(self, cx, cy, cradius):
        self.cr.circle((cx, cy), cradius, self.pen, self.brush)

    def draw_line(self, cx1, cy1, cx2, cy2):
        self.cr.line((cx1, cy1), (cx2, cy2), self.pen)

    def draw_path(self, cpoints):
        self.cr.path(cpoints, self.pen)

    ## def draw_image(self, cpoints, image):
    ##     img_data = image.get_data()
    ##     #self.cr.image(cpoints[0], img_np)

    ##     cut_lo, cut_hi = self.viewer.get_cut_levels()

    ##     print('drawing image')
    ##     #scene = self.viewer.view.scene

    ##     # get VisPy equivalent of our colormap
    ##     rgbmap = self.viewer.get_rgbmap()
    ##     g_cm = rgbmap.get_cmap()
    ##     g_cd = rgbmap.get_dist()
    ##     v_cm = VispyHelp.get_vispy_colormap(g_cm, g_cd)

    ##     ## image = scene.visuals.Image(img_data, interpolation='nearest',
    ##     ##                             cmap=v_cm,
    ##     ##                             clim=(cut_lo, cut_hi),
    ##     ##                             parent=scene, method='subdivide')
    ##     if len(self.viewer.visuals) == 0:
    ##         image = visuals.ImageVisual(img_data, interpolation='nearest',
    ##                                     cmap=v_cm,
    ##                                     clim=(cut_lo, cut_hi),
    ##                                     method='subdivide')
    ##         #image.transform = STTransform(scale=(1.0, 1.0), translate=(0, 0))
    ##         self.viewer.visuals.append(image)
    ##     #self.cr.ctx.draw_visual(image)
    ##     #self.cr.ctx.update()


class CanvasRenderer(object):

    def __init__(self, viewer):
        self.viewer = viewer

    def setup_cr(self, shape):
        cr = RenderContext(self.viewer)
        cr.initialize_from_shape(shape, font=False)
        return cr

    def get_dimensions(self, shape):
        cr = self.setup_cr(shape)
        cr.set_font_from_shape(shape)
        return cr.text_extents(shape.text)


#END
