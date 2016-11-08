#
# ImageViewVispy.py -- a backend for Ginga using Python Imaging Library
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.

import numpy
from io import BytesIO

from vispy import app
from vispy import scene
from vispy.geometry import Rect
import vispy.io as vio

#from . import VispyHelp
from ginga import Mixins, Bindings, colors
from ginga.vispyw import VispyHelp
from ginga.vispyw.CanvasRenderVispy import CanvasRenderer

from ginga import ImageView


class ImageViewVispyError(ImageView.ImageViewError):
    pass

class ImageViewVispy(ImageView.ImageViewBase):

    def __init__(self, logger=None, rgbmap=None, settings=None):
        ImageView.ImageViewBase.__init__(self, logger=logger,
                                         rgbmap=rgbmap,
                                         settings=settings)

        canvas = scene.SceneCanvas(create_native=True, show=False,
                                   bgcolor=self.img_bg)
        self.surface = canvas

        canvas.connect(self.on_resize)
        canvas.connect(self.on_draw)

        # Set up a viewbox to display the image with interactive pan/zoom
        view = canvas.central_widget.add_view()
        self.view = view

        # Set 2D camera (the camera will scale to the contents in the scene)
        view.camera = scene.PanZoomCamera(interactive=False, aspect=1)
        # flip y-axis to have correct aligment
        #view.camera.flip = (0, 1, 0)

        self.defer_redraw = True
        self._self_scaling = True
        self._rgb_order = 'RGBA'

        self.renderer = CanvasRenderer(self)

        self._vs_msg = scene.visuals.Text(text='', color='white',
                                          pos=(200, 200, 10),
                                          font_size=24,
                                          #transform=canvas.render_transform,
                                          parent=self.view.scene)
        self._vs_img = None

        # cursors
        self.cursor = {}

        wd, ht = canvas.size
        self.configure_window(wd, ht)

        # Create timers
        self._msg_timer = app.Timer(start=False, iterations=1)
        self._msg_timer.connect(lambda evt: self.onscreen_message_off())

        self._defer_timer = app.Timer(start=False, iterations=1)
        self._defer_timer.connect(self._update_cmap)

    def get_surface(self):
        return self.surface

    def get_widget(self):
        return self.surface.native
        #return self.surface.central_widget

    def configure_window(self, width, height):
        self.configure(width, height)

    def on_resize(self, event):
        """This callback is called by VisPy canvas when it is resized."""
        width, height = event.size

        self.configure_window(width, height)

    def on_draw(self, event):
        self.logger.info("draw!")

        pan_pos = self.get_pan()
        self.t_.set(pan=pan_pos, callback=False)
        #print(("pan", pan_pos))

        scale = self.get_scale_xy()
        self.t_.set(scale=scale, callback=False)
        #print(("scale", scale))

        rect = self.get_datarect()
        #print(("rect", rect))

    def get_rgb_image_as_buffer(self, output=None, format='png', quality=90):
        if self.surface is None:
            raise ImageViewVispyError("No VisPy surface defined")

        obuf = output
        if obuf is None:
            obuf = BytesIO()

        image = self.get_image_as_array()

        vio.imsave(obuf, image, format=format)

        if output is not None:
            return None
        return obuf.getvalue()

    def get_image_as_array(self):
        if self.surface is None:
            raise ImageViewVispyError("No VisPy surface defined")

        wd, ht = self.get_window_size()
        arr8 = self.surface.render(size=(wd, ht))
        return arr8

    def get_image_as_buffer(self, output=None):
        obuf = output
        if obuf is None:
            obuf = BytesIO()

        arr8 = self.get_image_as_array()
        obuf.write(arr8.tostring(order='C'))

        if not (output is None):
            return None
        return obuf.getvalue()

    def get_rgb_image_as_bytes(self, format='png', quality=90, output=None):
        if self.surface is None:
            raise ImageViewVispyError("No VisPy surface defined")

        obuf = output
        if obuf is None:
            obuf = BytesIO()

        wd, ht = self.get_window_size()
        image = self.surface.render(size=(wd, ht))

        vio.imsave(obuf, image, format=format)

        if not (output is None):
            return None
        return obuf.getvalue()

    def save_rgb_image_as_file(self, filepath, format='png', quality=90):
        with open(filepath, 'w') as out_f:
            self.get_rgb_image_as_bytes(output=out_f, format=format,
                                        quality=quality)
        self.logger.debug("wrote %s file '%s'" % (format, filepath))

    def update_image(self):
        #self.surface.update()

        ## scale = self.get_scale()
        ## pan_x, pan_y = self.get_pan()
        ## self.view.camera.zoom(scale, (pan_x, pan_y))
        return False

    def set_cursor(self, cursor):
        # subclass implements this method to actually set a defined
        # cursor on a widget
        self.logger.warning("Subclass should override this method")

    def reschedule_redraw(self, time_sec):
        try:
            self._defer_timer.stop()
        except:
            pass

        self._defer_timer.start(time_sec)

    def rescheduled_redraw(self, event):
        print("Time to redraw!")

    def define_cursor(self, ctype, cursor):
        self.cursor[ctype] = cursor

    def get_cursor(self, ctype):
        return self.cursor[ctype]

    def switch_cursor(self, ctype):
        self.set_cursor(self.cursor[ctype])

    def get_rgb_order(self):
        return self._rgb_order

    def onscreen_message(self, text, delay=None, redraw=True):
        try:
            self._msg_timer.stop()
        except:
            pass
        self._vs_msg.text = text
        if redraw:
            self._vs_msg.update()
        if delay:
            self._msg_timer.start(delay)

    def onscreen_message_off(self):
        self._vs_msg.text = ''
        self._vs_msg.update()

    ## def show_pan_mark(self, tf):
    ##     self.t_.set(show_pan_position=tf)
    ##     self.redraw(whence=3)

    #################################################################
    #   Overridden from base class, because the VisPy backend manages
    # its own canvas and drawing
    #################################################################

    def get_datarect(self):
        cam = self.view.camera
        rect = cam.rect
        pos_x, pos_y = rect.pos
        wd, ht = rect.size
        return (pos_x, pos_y, pos_x + wd, pos_y + ht)

    def get_pan(self):
        cam = self.view.camera
        rect = cam.rect
        pan_pos = rect.center[:2]
        return pan_pos

    def get_scale_xy(self):
        # calculate scale
        rect = self.get_datarect()
        win_wd, win_ht = self.get_window_size()
        wd = abs(rect[2] - rect[0])
        ht = abs(rect[3] - rect[1])
        scale_x = float(win_wd) / wd
        scale_y = float(win_ht) / ht
        return (scale_x, scale_y)

    def get_data_xy(self, win_x, win_y):
        # TODO: vectorize
        tfrm = self.view.camera.transform
        coord = numpy.array([win_x, win_y, 0, 1])
        pt = tfrm.imap(coord)
        data_x = float(pt[0]) - self.data_off
        data_y = float(pt[1]) - self.data_off
        return (data_x, data_y)

    def get_canvas_xy(self, data_x, data_y):
        # TODO: vectorize
        tfrm = self.view.camera.transform
        coord = numpy.array([data_x, data_y, 0, 1])
        pt = tfrm.map(coord)
        win_x = float(pt[0])
        win_y = float(pt[1])
        win_x += self.data_off
        win_y += self.data_off
        return (win_x, win_y)

    def pan_cb(self, setting, value):
        super(ImageViewVispy, self).pan_cb(setting, value)

        self.logger.info("setting pan to %s" % (str(value)))
        #pan_x, pan_y = value

        self.view.camera.center = value[:2]

        # HACK: seems to be necessary to force a camera update
        # on some platforms/versions
        self.view.camera.view_changed()

    def scale_cb(self, setting, value):
        super(ImageViewVispy, self).scale_cb(setting, value)

        pan_x, pan_y = self.get_pan()[:2]
        scale_x, scale_y = value[:2]

        self.logger.info("setting scale=%f pan=%f,%f" % (
            scale_x, pan_x, pan_y))

        rect = Rect(self.view.camera.rect)
        win_wd, win_ht = self.get_window_size()
        wd_2, ht_2 = win_wd / scale_x / 2., win_ht / scale_y / 2.
        rect.left, rect.right = pan_x - wd_2, pan_x + wd_2
        rect.bottom, rect.top = pan_y - ht_2, pan_y + ht_2

        self.view.camera.rect = rect

        #self.view.camera.view_changed()

    def transform_cb(self, setting, value):
        super(ImageViewVispy, self).transform_cb(setting, value)

        flipx, flipy, swapxy = self.get_transforms()

        # TODO: implement swapxy
        self.view.camera.flip = (flipx, flipy, False)

    def rotation_change_cb(self, setting, value):
        axis = [0, 0, 0]
        # no rotation possible with STTransform?
        #self.view.camera.transform.rotate(angle_deg, axis)

    def cut_levels_cb(self, setting, value):
        self.rgbmap_cb(self.get_rgbmap())

    def rgbmap_cb(self, rgbmap):
        self.logger.debug("updating rgbmap")
        super(ImageViewVispy, self).rgbmap_cb(rgbmap)

        if self._vs_img is None:
            return

        try:
            self._defer_timer.stop()
        except:
            pass

        time_sec = 0.020
        self._defer_timer.start(time_sec)

    def _update_cmap(self, event):
        self.logger.debug("updating color map and limits")
        cuts = self.get_cut_levels()
        cmap = VispyHelp.get_vispy_colormap(self.get_rgbmap())

        self._vs_img.clim = cuts
        self._vs_img.cmap = cmap

    def _image_set_cb(self, canvas_img, image):

        cuts = self.get_cut_levels()

        # get VisPy equivalent of our colormap
        if canvas_img.rgbmap is not None:
            rgbmap = canvas_img.rgbmap
        else:
            rgbmap = self.get_rgbmap()
        cmap = VispyHelp.get_vispy_colormap(rgbmap)

        if self._vs_img is None:
            parent = self.view.scene
            img_data = image.get_data()
            v_image = scene.visuals.Image(img_data, interpolation='nearest',
                                          cmap=cmap,
                                          clim=cuts,
                                          parent=parent, method='subdivide')
            self._vs_img = v_image
        else:
            self._vs_img.clim = cuts
            self._vs_img.cmap = cmap

        super(ImageViewVispy, self)._image_set_cb(canvas_img, image)

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

        # Hacky way to remove default SceneCanvas pan binding
        #print(dir(self.view.camera))
        #print(dir(self.view.camera._viewbox.events))
        self.view.camera._viewbox.events.mouse_move.disconnect(
            self.view.camera.viewbox_mouse_event)
        self.view.camera._viewbox.events.mouse_wheel.disconnect(
            self.view.camera.viewbox_mouse_event)
        self.view.camera._viewbox.events.key_press.disconnect(
            self.view.camera.viewbox_key_event)

        connect = self.surface.connect
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
        event.handled = True
        try:
            _keyname = event.key.name
        except AttributeError:
            # some keys (e.g. CapsLock) apparently don't have a name
            _keyname = event.key
        keytext = event.text
        keyname = self.transkey(_keyname, keytext)
        self.logger.debug("key press event, key=%s (%s)" % (keyname, keytext))
        if keyname is not None:
            self.make_ui_callback('key-press', keyname)
            return True

    def on_key_release(self, event):
        event.handled = True
        try:
            _keyname = event.key.name
        except AttributeError:
            # some keys (e.g. CapsLock) apparently don't have a name
            _keyname = event.key
        keytext = event.text
        keyname = self.transkey(_keyname, keytext)
        self.logger.debug("key release event, key=%s (%s)" % (keyname, keytext))
        if keyname is not None:
            self.make_ui_callback('key-release', keyname)
            return True

    def on_mouse_press(self, event):
        event.handled = True
        x, y = event.pos
        button = 0
        if event.button in (1, 2, 3):
            button |= 0x1 << (event.button - 1)
        self.logger.debug("button event at %dx%d, button=%x" % (x, y, button))

        data_x, data_y = self.get_data_xy(x, y)
        return self.make_ui_callback('button-press', button, data_x, data_y)

    def on_mouse_release(self, event):
        event.handled = True
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
        event.handled = True
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
        event.handled = True
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
