#
# ImageViewVispy.py -- a backend for Ginga using Vispy canvas
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.

import sys, os
import math
from io import BytesIO

import numpy as np

from vispy import app
from vispy import gloo
from vispy import visuals
from vispy.visuals.transforms import STTransform

#from ginga import ImageView
from ginga.pilw.ImageViewPil import (ImageViewPil as ImageView,
                                     ImageViewPilError as ImageViewError)
from ginga import Mixins, Bindings, colors
from ginga.vispyw.CanvasRenderVispy import CanvasRenderer


#class ImageViewVispyError(ImageView.ImageViewError):
class ImageViewVispyError(ImageViewError):
    pass

class ImageViewVispy(ImageView):

    def __init__(self, logger=None, rgbmap=None, settings=None):
        ImageView.__init__(self, logger=logger,
                           rgbmap=rgbmap,
                           settings=settings)

        canvas = app.Canvas(size=(600, 600))
        self._surface = canvas
        self._vpimage = None

        canvas.connect(self.on_resize)
        canvas.connect(self.on_draw)

        self.delayed_redraw = False

        # NOTE: vispy manages it's Y coordinates by default with
        # the origin at the bottom (see base class)
        self._originUpper = True

        self.img_fg = (1.0, 1.0, 1.0)
        self.img_bg = (0.5, 0.5, 0.5)

        # cursors
        self.cursor = {}

        # Create timers
        self._msg_timer = app.Timer(start=False, iterations=1)
        self._msg_timer.connect(lambda evt: self.onscreen_message_off())

        self._defer_timer = app.Timer(start=False, iterations=1)
        self._defer_timer.connect(lambda evt: self.delayed_redraw())

        wd, ht = canvas.size
        self.configure_window(wd, ht)

    def get_widget(self):
        return self._surface

    def get_rgb_order(self):
        return self._rgb_order

    def render_image(self, rgbobj, dst_x, dst_y):

        """Render the image represented by (rgbobj) at dst_x, dst_y
        in the pixel space.

        NOTE: this version uses a PlotWidget.image to render the image.
        """
        self.logger.debug("redraw surface")
        if self._surface is None:
            return

        # Grab the RGB array for the current image and place it in the
        # vispy Canvas
        #img_data = self.get_image_as_array()
        #img_data = self.getwin_array(order=self._rgb_order)
        img_data = self.getwin_array(order='RGBA')
        print(img_data.shape)
        print(np.mean(img_data[:, :, :2]))

        dst_x = dst_y = 0

        if self._vpimage is None:
            image = visuals.ImageVisual(img_data, interpolation='nearest',
                                        method='subdivide')
            image.transform = STTransform(scale=(1.0, 1.0), translate=(0, 0))
            self._vpimage = image
        else:
            self._vpimage.set_data(img_data)
            self._vpimage.update()

        #self._surface.update()
        print("added image")

    def on_draw(self, event):
        self.logger.info("draw!")

        pan_pos = self.get_pan()
        print(("pan", pan_pos))
        #self._t.set(pan=)

        rect = self.get_datarect()
        print(("rect", rect))

    def configure_window(self, width, height):
        #self.configure(width, height)
        self.configure_surface(width, height)

    def on_resize(self, event):
        """This callback is called by VisPy canvas when it is resized."""
        width, height = event.size

        # Set canvas viewport and reconfigure visual transforms to match.
        canvas = self._surface
        #vp = (0, 0, canvas.physical_size[0], canvas.physical_size[1])
        vp = (0, 0, width, height)
        canvas.context.set_viewport(*vp)
        if self._vpimage is not None:
            self._vpimage.transforms.configure(canvas=canvas, viewport=vp)

        self.configure_window(width, height)

    def get_png_image_as_buffer(self, output=None):
        ibuf = output
        if ibuf is None:
            ibuf = BytesIO()
        qimg = self.surface.write_to_png(ibuf)
        return ibuf

    def update_image(self):
        self.logger.info("update image")
        gloo.clear(color=self.img_bg, depth=True)

        self._vpimage.draw()
        self._surface.update()

    def set_cursor(self, cursor):
        pass

    def define_cursor(self, ctype, cursor):
        self.cursor[ctype] = cursor

    def get_cursor(self, ctype):
        return self.cursor[ctype]

    def switch_cursor(self, ctype):
        self.set_cursor(self.cursor[ctype])

    def set_fg(self, r, g, b):
        self.img_fg = (r, g, b)
        self.redraw(whence=3)

    def onscreen_message(self, text, delay=None):
        try:
            self._msg_timer.stop()
        except:
            pass

        self.set_onscreen_message(text)
        self.redraw(whence=3)

        if delay:
            time_ms = int(delay * 1000.0)
            self._msg_timer.interval = time_ms
            self._msg_timer.start()

    def onscreen_message_off(self):
        return self.onscreen_message(None)

    def reschedule_redraw(self, time_sec):

        if self._defer_timer is None:
            self.delayed_redraw()
            return

        try:
            self._defer_timer.stop()
        except:
            pass

        time_ms = int(time_sec * 1000)
        try:
            self._defer_timer.interval = time_ms
            self._defer_timer.start()

        except Exception as e:
            self.logger.warning("Exception starting timer: %s; "
                             "using unoptomized redraw" % (str(e)))
            self.delayed_redraw()

    def _delayed_redraw(self, event):
        return self.delayed_redraw()


class ImageViewEvent(ImageViewVispy):

    def __init__(self, logger=None, rgbmap=None, settings=None):
        ImageViewVispy.__init__(self, logger=logger, rgbmap=rgbmap,
                                settings=settings)

        # last known window mouse position
        self.last_win_x = 0
        self.last_win_y = 0
        # last known data mouse position
        self.last_data_x = 0
        self.last_data_y = 0
        # Does widget accept focus when mouse enters window
        self.enter_focus = self.t_.get('enter_focus', True)

        # vispy/ginga key mapping
        self._keytbl = {
            'shift': 'shift_l',
            'control': 'control_l',
            'alt': 'alt_l',
            'win': 'super_l',
            '`': 'backquote',
            '"': 'doublequote',
            "'": 'singlequote',
            '\\': 'backslash',
            ' ': 'space',
            # NOTE: not working
            'escape': 'escape',
            'enter': 'return',
            # NOTE: not working
            'tab': 'tab',
            # NOTE: all Fn keys not working
            'f1': 'f1',
            'f2': 'f2',
            'f3': 'f3',
            'f4': 'f4',
            'f5': 'f5',
            'f6': 'f6',
            'f7': 'f7',
            'f8': 'f8',
            'f9': 'f9',
            'f10': 'f10',
            'f11': 'f11',
            'f12': 'f12',
            }

        # Define cursors for pick and pan
        #hand = openHandCursor()
        hand = 0
        self.define_cursor('pan', hand)
        #cross = thinCrossCursor('aquamarine')
        cross = 1
        self.define_cursor('pick', cross)

        connect = self._surface.connect
        connect(self.on_initialize)
        #connect(self.on_focus)
        #connect(self.on_blur)
        #connect(self.on_enter)
        #connect(self.on_leave)
        connect(self.on_mouse_move)
        connect(self.on_mouse_press)
        connect(self.on_mouse_release)
        connect(self.on_key_press)
        connect(self.on_key_release)
        connect(self.on_mouse_wheel)

        # TODO: drag-drop event
        for name in ('motion', 'button-press', 'button-release',
                     'key-press', 'key-release', 'drag-drop',
                     'scroll', 'map', 'focus', 'enter', 'leave',
                     ):
            self.enable_callback(name)


    def on_initialize(self, event):
        return self.make_callback('map')

    def transkey(self, keyname, keytext):
        self.logger.debug("vispy keyname='%s'" % (keyname))
        if keyname is None:
            return keyname
        try:
            return self._keytbl[keyname.lower()]

        except KeyError:
            return keytext

    def get_keyTable(self):
        return self._keytbl

    def set_enter_focus(self, tf):
        self.enter_focus = tf

    def on_focus(self, event, hasFocus):
        return self.make_callback('focus', hasFocus)

    def on_enter(self, event):
        if self.enter_focus:
            self.focus_event(event, True)
        return self.make_callback('enter')

    def on_leave(self, event):
        self.logger.debug("leaving widget...")
        if self.enter_focus:
            self.focus_event(event, False)
        return self.make_callback('leave')

    def on_key_press(self, event):
        _keyname = event.key.name
        keytext = event.text
        keyname = self.transkey(_keyname, keytext)
        self.logger.debug("key press event, key=%s (%s)" % (keyname, keytext))
        if keyname is not None:
            self.make_ui_callback('key-press', keyname)
            return True

    def on_key_release(self, event):
        _keyname = event.key.name
        keytext = event.text
        keyname = self.transkey(_keyname, keytext)
        self.logger.debug("key release event, key=%s (%s)" % (keyname, keytext))
        if keyname is not None:
            self.make_ui_callback('key-release', keyname)
            return True

    def on_mouse_press(self, event):
        x, y = event.pos
        button = 0
        if event.button in (1, 2, 3):
            button |= 0x1 << (event.button - 1)
        self.logger.debug("button event at %dx%d, button=%x" % (x, y, button))

        data_x, data_y = self.get_data_xy(x, y)
        return self.make_ui_callback('button-press', button, data_x, data_y)

    def on_mouse_release(self, event):
        x, y = event.pos
        button = 0
        if event.button in (1, 2, 3):
            button |= 0x1 << (event.button - 1)
        self.logger.debug("button release at %dx%d button=%x" % (x, y, button))

        data_x, data_y = self.get_data_xy(x, y)
        return self.make_ui_callback('button-release', button, data_x, data_y)

    def get_last_win_xy(self):
        return (self.last_win_x, self.last_win_y)

    def get_last_data_xy(self):
        return (self.last_data_x, self.last_data_y)

    def on_mouse_move(self, event):
        button = 0
        x, y = event.pos
        self.last_win_x, self.last_win_y = x, y

        if event.button in (1, 2, 3):
            button |= 0x1 << (event.button - 1)
        self.logger.debug("motion event at %dx%d, button=%x" % (x, y, button))

        data_x, data_y = self.get_data_xy(x, y)
        self.last_data_x, self.last_data_y = data_x, data_y
        self.logger.debug("motion event at DATA %dx%d" % (data_x, data_y))

        return self.make_ui_callback('motion', button, data_x, data_y)

    def on_mouse_wheel(self, event):
        x, y = event.pos
        direction, amount = event.delta
        #print(('wheel', amount, direction))

        if amount >= 0:
            direction = 0.0
        elif amount < 0:
            direction = 180.0
        amount = abs(amount)
        self.logger.debug("scroll amount=%f direction=%f" % (
            amount, direction))

        data_x, data_y = self.get_data_xy(x, y)
        self.last_data_x, self.last_data_y = data_x, data_y

        return self.make_ui_callback('scroll', direction, amount,
                                  data_x, data_y)

class ImageViewZoom(Mixins.UIMixin, ImageViewEvent):

    # class variables for binding map and bindings can be set
    bindmapClass = Bindings.BindingMapper
    bindingsClass = Bindings.ImageViewBindings

    @classmethod
    def set_bindingsClass(cls, klass):
        cls.bindingsClass = klass

    @classmethod
    def set_bindmapClass(cls, klass):
        cls.bindmapClass = klass

    def __init__(self, logger=None, rgbmap=None, settings=None,
                 bindmap=None, bindings=None):
        ImageViewEvent.__init__(self, logger=logger, rgbmap=rgbmap,
                                settings=settings)
        Mixins.UIMixin.__init__(self)

        self.ui_setActive(True)

        if bindmap is None:
            bindmap = ImageViewZoom.bindmapClass(self.logger)
        self.bindmap = bindmap
        bindmap.register_for_events(self)

        if bindings is None:
            bindings = ImageViewZoom.bindingsClass(self.logger)
        self.set_bindings(bindings)

    def get_bindmap(self):
        return self.bindmap

    def get_bindings(self):
        return self.bindings

    def set_bindings(self, bindings):
        self.bindings = bindings
        bindings.set_bindings(self)


class CanvasView(ImageViewZoom):

    def __init__(self, logger=None, settings=None, rgbmap=None,
                 bindmap=None, bindings=None):
        ImageViewZoom.__init__(self, logger=logger, settings=settings,
                               rgbmap=rgbmap,
                               bindmap=bindmap, bindings=bindings)

        # Needed for UIMixin to propagate events correctly
        self.objects = [self.private_canvas]

    def set_canvas(self, canvas, private_canvas=None):
        super(CanvasView, self).set_canvas(canvas,
                                           private_canvas=private_canvas)

        self.objects[0] = self.private_canvas


#END
