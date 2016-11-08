#! /usr/bin/env python
#
# gview.py -- Simple, configurable FITS viewer.
#
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
from __future__ import print_function
import sys, os
import glob
import time
import logging
import threading
import math
import numpy

from astropy.io import fits

from ginga import AstroImage, colors
from ginga.canvas.CanvasObject import get_canvas_types
from ginga.misc import log, Bunch, Task
from ginga.util import mosaic, plots
from ginga.util import wcs, iqcalc, dp
from ginga.util import grc
from ginga.web.pgw import Widgets, Viewers, Plot
from ginga.misc.plugins.Command import CommandInterpreter
from ginga import cmap
# add any matplotlib colormaps we have lying around
cmap.add_matplotlib_cmaps(fail_on_import_error=False)

from naoj.spcam.spcam_dr import SuprimeCamDR
from naoj.hsc.hsc_dr import HyperSuprimeCamDR, hsc_ccd_data
# add "Jon Tonley" color map
from naoj.cmap import jt
cmap.add_cmap("jt", jt.cmap_jt)


class GView(object):

    def __init__(self, logger, window, thread_pool):
        self.logger = logger
        self.threadPool = thread_pool

        self.cmd_w = None
        self.hist_w = None
        self.histlimit = 5000

        self.plot = None
        self.plot_w = None
        self.viewer = None

        self._cmdobj = GViewInterpreter(self, self)

        self.dc = get_canvas_types()

        # desired dimensions of the viewer
        self.wd = 800
        self.ht = 800

        self.top = window
        self.top.add_callback('close', self.closed)

        # For asynchronous tasks on the thread pool
        self.tag = 'master'
        self.shares = ['threadPool', 'logger']

        self.build_gui()

    def build_gui(self):
        vbox = Widgets.VBox()
        vbox.set_border_width(2)
        vbox.set_spacing(1)

        fi = Viewers.CanvasView(self.logger)
        fi.enable_autocuts('on')
        fi.set_autocut_params('zscale')
        fi.enable_autozoom('on')
        fi.set_zoom_algorithm('rate')
        fi.set_color_map('gray')
        fi.set_zoomrate(1.6)
        fi.show_pan_mark(True)
        #fi.set_callback('drag-drop', self.drop_file)
        fi.set_callback('none-move', self.motion)
        fi.set_bg(0.2, 0.2, 0.2)
        fi.ui_setActive(True)
        self.viewer = fi

        bd = fi.get_bindings()
        bd.enable_all(True)

        # canvas that we will draw on
        canvas = self.dc.DrawingCanvas()
        ## canvas.enable_draw(True)
        ## canvas.enable_edit(True)
        ## canvas.set_drawtype('rectangle', color='lightblue')
        canvas.setSurface(fi)
        self.canvas = canvas
        # add canvas to view
        private_canvas = fi.get_canvas()
        private_canvas.add(canvas)
        canvas.ui_setActive(True)
        ## canvas.set_callback('draw-event', self.draw_cb)
        ## canvas.set_callback('edit-event', self.edit_cb)
        ## canvas.add_draw_mode('move', down=self.btndown,
        ##                      move=self.drag, up=self.update)
        ## canvas.register_for_cursor_drawing(fi)
        ## canvas.set_draw_mode('move')
        self.drawtypes = canvas.get_drawtypes()
        self.drawtypes.sort()

        # add a color bar
        #private_canvas.add(self.dc.ColorBar(side='bottom', offset=10))

        # add little mode indicator that shows modal states in
        # the corner
        private_canvas.add(self.dc.ModeIndicator(corner='ur', fontsize=14))
        # little hack necessary to get correct operation of the mode indicator
        # in all circumstances
        bm = fi.get_bindmap()
        bm.add_callback('mode-set', lambda *args: fi.redraw(whence=3))

        fi.set_desired_size(self.wd, self.ht)
        w = Viewers.GingaViewerWidget(viewer=fi)
        w.resize(self.wd, self.ht)
        vbox.add_widget(w, stretch=1)

        self._cmdobj.register_viewer(fi)

        self.readout = Widgets.Label("")
        self.readout.set_font('monospace 12')
        self.readout.set_color(fg='green')
        vbox.add_widget(self.readout, stretch=0)

        hbox = Widgets.HBox()
        hbox.set_spacing(4)

        hbox.add_widget(Widgets.Label('Zoom sensitivity: '))
        slider = Widgets.Slider(orientation='horizontal', dtype=float)
        slider.add_callback('value-changed',
                            lambda w, val: self.adjust_scrolling_accel_cb(val))
        slider.set_limits(0.0, 12.0, 0.005)
        slider.set_value(10.0)
        hbox.add_widget(slider, stretch=1)
        #hbox.add_widget(Widgets.Label(''), stretch=1)
        vbox.add_widget(hbox, stretch=0)

        bhbox = Widgets.HBox()
        bhbox.add_widget(vbox)

        # add the plots
        gbox = Widgets.GridBox()

        # This is the plot
        hbox = Widgets.HBox()
        wd, ht = 800, 600
        self._plot = plots.Plot(logger=self.logger,
                                width=wd, height=ht)
        self._cmdobj._plot = self._plot

        pw = Plot.PlotWidget(self._plot)
        pw.name = "plot"
        pw.resize(wd, ht)
        self._cmdobj._plot_w = pw

        hbox.add_widget(pw, stretch=1)
        gbox.add_widget(hbox, 0, 0)

        vbox2 = Widgets.VBox()
        self.cmd_w = Widgets.TextEntry()
        self.cmd_w.add_callback('activated', self.exec_cmd_cb)
        vbox2.add_widget(self.cmd_w, stretch=0)

        self.hist_w = Widgets.TextArea()
        vbox2.add_widget(self.hist_w, stretch=1)
        gbox.add_widget(vbox2, 1, 0)

        bhbox.add_widget(gbox)

        self.top.set_widget(bhbox)

    def set_data_dir(self, path):
        self.basedir = path
        self.logger.info("Data directory set to '%s'" % (path))

    def set_flat_dir(self, path):
        self.flat_dir = path
        self.logger.info("Flat directory set to '%s'" % (path))
        self.use_flat = True

    def clear_canvas(self):
        self.canvas.delete_all_objects()

    def motion(self, viewer, button, data_x, data_y):

        # Get the value under the data coordinates
        try:
            #value = viewer.get_data(data_x, data_y)
            # We report the value across the pixel, even though the coords
            # change halfway across the pixel
            value = viewer.get_data(int(data_x+0.5), int(data_y+0.5))

        except Exception:
            value = None

        fits_x, fits_y = data_x + 1, data_y + 1

        # Calculate WCS RA
        try:
            # NOTE: image function operates on DATA space coords
            image = viewer.get_image()
            if image is None:
                # No image loaded
                return
            ra_txt, dec_txt = image.pixtoradec(fits_x, fits_y,
                                               format='str', coords='fits')
        except Exception as e:
            self.logger.warning("Bad coordinate conversion: %s" % (
                str(e)))
            ra_txt  = 'BAD WCS'
            dec_txt = 'BAD WCS'

        text = "RA: %s  DEC: %s  X: %.2f  Y: %.2f  Value: %s" % (
            ra_txt, dec_txt, fits_x, fits_y, value)
        self.readout.set_text(text)


    def exec_cmd(self, text):
        text = text.strip()
        self.log("g> " + text, w_time=True)

        if text.startswith('!'):
            # escape to shell for this command
            #self.exec_shell(text[1:])
            return

        args = text.split()
        cmd, tokens = args[0], args[1:]

        # process args
        args, kwargs = grc.prep_args(tokens)

        try:
            method = getattr(self._cmdobj, "cmd_" + cmd.lower())

        except AttributeError:
            self.log("|E| No such command: '%s'" % (cmd))
            return

        try:
            res = method(*args, **kwargs)
            if res is not None:
                self.log(str(res))

            # this brings the focus back to the command bar if the command
            # causes a new window to be opened
            self.cmd_w.focus()

        except Exception as e:
            self.log("|E| Error executing '%s': %s" % (text, str(e)))
            # TODO: add traceback


    def exec_cmd_cb(self, w):
        text = w.get_text()
        self.exec_cmd(text)
        w.set_text("")

    def exec_shell(self, cmd_str):
        res, out, err = grc.get_exitcode_stdout_stderr(cmd_str)
        if len(out) > 0:
            self.log(out.decode('utf-8'))
        if len(err) > 0:
            self.log(err.decode('utf-8'))
        if res != 0:
            self.log("command terminated with error code %d" % res)

    def log(self, text, w_time=False):
        if self.hist_w is not None:
            pfx = ''
            if w_time:
                pfx = time.strftime("%H:%M:%S", time.localtime()) + ": "
            self.hist_w.append_text(pfx + text + '\n',
                                    autoscroll=True)
            #self.fv.update_pending()

    def adjust_scrolling_accel_cb(self, val):
        def f(x):
            return (1.0 / 2.0**(10.0-x))
        val2 = f(val)
        self.logger.debug("slider value is %f, setting will be %f" % (val, val2))
        settings = self.viewer.get_bindings().get_settings()
        settings.set(scroll_zoom_acceleration=val2)
        return True

    def closed(self, w):
        self.logger.info("Top window closed.")
        self.top = None
        sys.exit()

    def quit(self, *args):
        self.readout.set_text("Quitting!")
        self.logger.info("Attempting to shut down the application...")
        if not self.top is None:
            self.top.close()
        sys.exit()

class GViewInterpreter(CommandInterpreter):

    def __init__(self, fv, plugin):
        super(GViewInterpreter, self).__init__(fv, plugin)

        self._view = None
        self.buffers = Bunch.Bunch()

        self.iqcalc = iqcalc.IQCalc(self.logger)
        self._plot = None
        self._plot_w = None

        # Peak finding parameters and selection criteria
        self.radius = 20
        # for contour plot
        self.contour_radius = 6
        self.settings = {}
        self.max_side = self.settings.get('max_side', 1024)
        self.radius = self.settings.get('radius', 10)
        self.threshold = self.settings.get('threshold', None)
        self.min_fwhm = self.settings.get('min_fwhm', 2.0)
        self.max_fwhm = self.settings.get('max_fwhm', 50.0)
        self.min_ellipse = self.settings.get('min_ellipse', 0.5)
        self.edgew = self.settings.get('edge_width', 0.01)
        # Report in 0- or 1-based coordinates
        self.pixel_coords_offset = self.settings.get('pixel_coords_offset',
                                                     0.0)

        self.hsc_dr = HyperSuprimeCamDR(logger=self.logger)

        self.sub_bias = True
        # For flat fielding
        self.flat = {}
        self.flat_dir = '.'
        self.flat_filter = None
        self.use_flat = False

    def register_viewer(self, viewer):
        self._view = viewer
        fi = viewer
        bm = fi.get_bindmap()

        # add a new "zview" mode
        bm.add_mode('z', 'zview', mode_type='locked', msg=None)

        # zview had this kind of zooming function
        bm.map_event('zview', (), 'ms_left', 'zoom_in')
        bm.map_event('zview', (), 'ms_right', 'zoom_out')
        bm.map_event('zview', ('ctrl',), 'ms_left', 'zoom_out')

        # borrow some bindings from pan mode
        bm.map_event('zview', (), 'kp_left', 'pan_left')
        bm.map_event('zview', (), 'kp_right', 'pan_right')
        bm.map_event('zview', (), 'kp_up', 'pan_up')
        bm.map_event('zview', (), 'kp_down', 'pan_down')
        bm.map_event('zview', (), 'kp_s', 'pan_zoom_save')
        bm.map_event('zview', (), 'kp_1', 'pan_zoom_set')

        bm.map_event('zview', (), 'kp_p', 'radial-plot')
        bm.map_event('zview', (), 'kp_r', 'radial-plot')
        fi.set_callback('keydown-radial-plot',
                        self.plot_cmd_cb, self.do_radial_plot,
                        "Radial Profile")
        bm.map_event('zview', (), 'kp_e', 'contour-plot')
        fi.set_callback('keydown-contour-plot',
                        self.plot_cmd_cb, self.do_contour_plot,
                        "Contours")
        bm.map_event('zview', (), 'kp_g', 'gaussians-plot')
        fi.set_callback('keydown-gaussians-plot',
                        self.plot_cmd_cb, self.do_gaussians_plot,
                        "FWHM")

        # bindings customizations
        bd = fi.get_bindings()
        settings = bd.get_settings()

        # ZVIEW has a faster zoom ratio, by default
        settings.set(scroll_zoom_direct_scale=True,
                     scroll_zoom_acceleration=0.9)


    ##### COMMANDS #####

    def cmd_rd(self, bufname, path, *args):
        """rd bufname path

        Read file from `path` into buffer `bufname`.  If the buffer does
        not exist it will be created.

        If `path` does not begin with a slash it is assumed to be relative
        to the current working directory.
        """
        if not path.startswith('/'):
            path = os.path.join(os.getcwd(), path)
        if bufname in self.buffers:
            self.log("Buffer %s is in use. Will discard the previous data" % (
                bufname))
            image = self.buffers[bufname]
        else:
            # new buffer
            image = AstroImage.AstroImage(logger=self.logger)
            self.buffers[bufname] = image

        self.log("Reading file...(%s)" % (path))
        image.load_file(path)
        # TODO: how to know if there is an error
        self.log("File read")

    def cmd_tv(self, bufname, *args):
        """tv bufname [min max] [colormap]

        Display buffer `bufname` in the current viewer.  If no viewer
        exists one will be created.

        Optional:
        `min` and `max` specify lo/hi cut levels to scale the image
        data for display.

        `colormap` specifies a color map to use for the image.
        """
        if not bufname in self.buffers:
            self.log("!! No such buffer: '%s'" % (bufname))
            return
        image = self.buffers[bufname]

        if self._view is None:
            self.make_viewer("GView")

        self._view.set_image(image)

        gw = self._view

        args = list(args)

        locut = None
        if len(args) > 0:
            try:
                locut = float(args[0])
                hicut = float(args[1])
                args = args[2:]
            except ValueError:
                pass

        if locut is not None:
            gw.cut_levels(locut, hicut)

        if 'bw' in args:
            # replace "bw" with gray colormap
            i = args.index('bw')
            args[i] = 'gray'

        if len(args) > 0:
            cm_name = args[0]
            if cm_name == 'inv':
                gw.invert_cmap()
            else:
                gw.set_color_map(cm_name)

    def cmd_head(self, bufname, *args):
        """head buf [kwd ...]

        List the headers for the image in the named buffer.
        """
        if bufname not in self.buffers:
            self.log("No such buffer: '%s'" % (bufname))
            return

        image = self.buffers[bufname]
        header = image.get_header()
        res = []
        # TODO: include the comments
        if len(args) > 0:
            for kwd in args:
                if not kwd in header:
                    res.append("%-8.8s  -- NOT FOUND IN HEADER --" % (kwd))
                else:
                    res.append("%-8.8s  %s" % (kwd, str(header[kwd])))
        else:
            for kwd in header.keys():
                res.append("%-8.8s  %s" % (kwd, str(header[kwd])))

        self.log('\n'.join(res))

    def cmd_exps(self, n=20, hdrs=None):
        """exps  [n=20, time=]

        List the last n exposures in the current directory
        """
        cwd = os.getcwd()
        files = glob.glob(cwd + '/HSCA*[0,2,4,6,8]00.fits')
        files.sort()

        n = int(n)
        files = files[-n:]

        res = []
        for filepath in files:
            with fits.open(filepath, 'readonly', memmap=False) as in_f:
                header = in_f[0].header
            line = "%(EXP-ID)-12.12s  %(HST-STR)12.12s  %(OBJECT)14.14s  %(FILTER01)8.8s" % header

            # add user specified headers
            if hdrs is not None:
                for kwd in hdrs.split(','):
                    fmt = "%%(%s)12.12s" % kwd
                    line += '  ' + (fmt % header)
            res.append(line)

        self.log('\n'.join(res))

    def cmd_lsb(self):
        """lsb

        List the buffers
        """
        names = list(self.buffers.keys())
        names.sort()

        if len(names) == 0:
            self.log("No buffers")
            return

        res = []
        for name in names:
            d = self.get_buffer_info(name)
            d.size = "%dx%d" % (d.width, d.height)
            res.append("%(name)-10.10s  %(size)13s  %(path)s" % d)
        self.log("\n".join(res))

    def cmd_rmb(self, *args):
        """rmb NAME ...

        Remove buffer NAME
        """
        for name in args:
            if name in self.buffers:
                del self.buffers[name]
            else:
                self.log("No such buffer: '%s'" % (name))
        self.cmd_lsb()

    def cmd_rm(self, *args):
        """command to be deprecated--use 'rmb'
        """
        self.log("warning: this command will be deprecated--use 'rmb'")
        self.cmd_rmb(*args)

    def _ql(self, bufname, glob_pat, dr):
        if isinstance(glob_pat, str):
            pattern = "%s/%s" % (os.getcwd(), glob_pat)
            files = glob.glob(pattern)
        else:
            # arg is a "visit" number
            exp_num = int(str(int(glob_pat)) + "00")
            files = dr.exp_num_to_file_list(os.getcwd(), exp_num)

        fov_deg = dr.fov

        # read first image to seed mosaic
        seed = files[0]
        self.logger.debug("Reading seed image '%s'" % (seed))
        image = AstroImage.AstroImage(logger=self.logger)
        image.load_file(seed, memmap=False)

        name = 'mosaic'
        self.logger.debug("Preparing blank mosaic")

        if bufname in self.buffers:
            self.log("Buffer %s is in use. Will discard the previous data" % (
                bufname))
            del self.buffers[bufname]

        # new buffer
        mosaic_img = self.prepare_mosaic(image, fov_deg, name=name)
        self.buffers[bufname] = mosaic_img

        self.mosaic(files, mosaic_img, fov_deg=fov_deg, dr=dr, merge=True)

    def cmd_ql(self, bufname, glob_pat, *args):
        """ql bufname glob_pat
        """
        self._ql(bufname, glob_pat, self.spcam_dr)

    def cmd_hql(self, bufname, glob_pat, *args):
        """hql bufname glob_pat
        """
        self._ql(bufname, glob_pat, self.hsc_dr)

    def cmd_bias(self, *args):
        """bias on | off
        """
        if len(args) == 0:
            self.log("bias %s" % (self.sub_bias))
            return
        res = str(args[0]).lower()
        if res in ('y', 'yes', 't', 'true', '1', 'on'):
            self.sub_bias = True
        elif res in ('n', 'no', 'f', 'false', '0', 'off'):
            self.sub_bias = False
        else:
            self.log("Don't understand parameter '%s'" % (onoff))

    def cmd_flat(self, *args):
        """flat on | off
        """
        if len(args) == 0:
            self.log("flat %s" % (self.use_flat))
            return
        res = str(args[0]).lower()
        if res in ('y', 'yes', 't', 'true', '1', 'on'):
            self.use_flat = True
        elif res in ('n', 'no', 'f', 'false', '0', 'off'):
            self.use_flat = False
        else:
            self.log("Don't understand parameter '%s'" % (onoff))

    def cmd_flatdir(self, *args):
        """flatdir /some/path/to/flats
        """
        if len(args) > 0:
            path = str(args[0])
            if not os.path.isdir(path):
                self.log("Not a directory: %s" % (path))
                return
            self.flat_dir = path
        self.log("using (%s) for flats" % (self.flat_dir))

    def get_buffer_info(self, name):
        image = self.buffers[name]
        path = image.get('path', "None")
        res = Bunch.Bunch(dict(name=name, path=path, width=image.width,
                               height=image.height))
        return res

    def make_viewer(self, name):
        if self.fv.has_channel(name):
            channel = self.fv.get_channel(name)
        else:
            channel = self.fv.add_channel(name, num_images=0)

        self._view = channel
        return channel

    def cmd_resize(self, width, height):
        self._view.resize(int(width), int(height))

    ##### PLOTS #####

    def initialize_plot(self):
        wd, ht = 800, 600
        self._plot = plots.Plot(logger=self.logger,
                                width=wd, height=ht)

        pw = Plot.PlotWidget(self._plot)
        pw.resize(wd, ht)

        self._plot_w = self.fv.make_window("Plots")
        self._plot_w.set_widget(pw)
        self._plot_w.show()

    def plot_cmd_cb(self, viewer, event, data_x, data_y, fn, title):
        try:
            fn(viewer, event, data_x, data_y)

            #self._plot_w.set_title(title)
            #self._plot_w.raise_()
        finally:
            # this keeps the focus on the viewer widget, in case a new
            # window was popped up
            #viewer.get_widget().focus()
            pass

    def make_contour_plot(self):
        if self._plot is None:
            self.initialize_plot()

        fig = self._plot.get_figure()
        fig.clf()

        # Replace plot with Contour plot
        self._plot = plots.ContourPlot(logger=self.logger,
                                       figure=fig,
                                       width=600, height=600)
        self._plot.add_axis(axisbg='black')
        self._plot_w.set_plot(self._plot)

    def do_contour_plot(self, viewer, event, data_x, data_y):
        self.log("d> (contour plot)", w_time=True)
        try:
            results = self.find_objects(viewer, data_x, data_y)
            qs = results[0]
            x, y = qs.objx, qs.objy

        except Exception as e:
            self.log("No objects found")
            # we can still proceed with a contour plot at the point
            # where the key was pressed
            x, y = data_x, data_y

        self.make_contour_plot()

        image = viewer.get_image()
        self._plot.plot_contours(x, y, self.contour_radius, image,
                                 num_contours=12)
        return True


    def make_gaussians_plot(self):
        if self._plot is None:
            self.initialize_plot()

        fig = self._plot.get_figure()
        fig.clf()

        # Replace plot with FWHM gaussians plot
        self._plot = plots.FWHMPlot(logger=self.logger,
                                    figure=fig,
                                    width=600, height=600)
        self._plot.add_axis(axisbg='white')
        self._plot_w.set_plot(self._plot)

    def do_gaussians_plot(self, viewer, event, data_x, data_y):
        self.log("d> (gaussians plot)", w_time=True)
        try:
            results = self.find_objects(viewer, data_x, data_y)
            qs = results[0]

        except Exception as e:
            self.log("No objects found")
            return

        self.make_gaussians_plot()

        image = viewer.get_image()
        x, y = qs.objx, qs.objy

        self._plot.plot_fwhm(x, y, self.radius, image)
        return True

    def make_radial_plot(self):
        if self._plot is None:
            self.initialize_plot()

        fig = self._plot.get_figure()
        fig.clf()

        # Replace plot with Radial profile plot
        self._plot = plots.RadialPlot(logger=self.logger,
                                       figure=fig,
                                       width=700, height=600)
        self._plot.add_axis(axisbg='white')
        self._plot_w.set_plot(self._plot)

    def do_radial_plot(self, viewer, event, data_x, data_y):
        self.log("d> (radial plot)", w_time=True)
        try:
            results = self.find_objects(viewer, data_x, data_y)
            qs = results[0]

        except Exception as e:
            self.log("No objects found")
            return

        self.make_radial_plot()

        image = viewer.get_image()
        x, y = qs.objx, qs.objy

        self._plot.plot_radial(x, y, self.radius, image)

        rpt = self.make_report(image, qs)
        self.log("seeing size %5.2f" % (rpt.starsize))
        # TODO: dump other stats from the report

        # write seeing measurement in upper right corner
        ax = self._plot.ax
        ax.text(0.75, 0.85, "seeing: %5.2f" % (rpt.starsize),
                bbox=dict(facecolor='green', alpha=0.4, pad=6),
                ha='left', va='center', transform=ax.transAxes,
                fontsize=12)
        self._plot.draw()

        return True

    def find_objects(self, viewer, x, y):
        #x, y = viewer.get_last_data_xy()
        image = viewer.get_image()

        msg, results, qs = None, [], None
        try:
            data, x1, y1, x2, y2 = image.cutout_radius(x, y, self.radius)

            # Find bright peaks in the cutout
            self.logger.debug("Finding bright peaks in cutout")
            peaks = self.iqcalc.find_bright_peaks(data,
                                                  threshold=self.threshold,
                                                  radius=self.radius)
            num_peaks = len(peaks)
            if num_peaks == 0:
                raise Exception("Cannot find bright peaks")

            # Evaluate those peaks
            self.logger.debug("Evaluating %d bright peaks..." % (num_peaks))
            objlist = self.iqcalc.evaluate_peaks(peaks, data,
                                                 fwhm_radius=self.radius)

            num_candidates = len(objlist)
            if num_candidates == 0:
                raise Exception("Error evaluating bright peaks: no candidates found")

            self.logger.debug("Selecting from %d candidates..." % (num_candidates))
            height, width = data.shape
            results = self.iqcalc.objlist_select(objlist, width, height,
                                                 minfwhm=self.min_fwhm,
                                                 maxfwhm=self.max_fwhm,
                                                 minelipse=self.min_ellipse,
                                                 edgew=self.edgew)
            if len(results) == 0:
                raise Exception("No object matches selection criteria")

            # add back in offsets from cutout to result positions
            for qs in results:
                qs.x += x1
                qs.y += y1
                qs.objx += x1
                qs.objy += y1

        except Exception as e:
            msg = str(e)
            self.logger.error("Error finding object: %s" % (msg))
            raise e

        return results

    def make_report(self, image, qs):
        d = Bunch.Bunch()
        try:
            x, y = qs.objx, qs.objy
            equinox = float(image.get_keyword('EQUINOX', 2000.0))

            try:
                ra_deg, dec_deg = image.pixtoradec(x, y, coords='data')
                ra_txt, dec_txt = wcs.deg2fmt(ra_deg, dec_deg, 'str')

            except Exception as e:
                self.logger.warning("Couldn't calculate sky coordinates: %s" % (str(e)))
                ra_deg, dec_deg = 0.0, 0.0
                ra_txt = dec_txt = 'BAD WCS'

            # Calculate star size from pixel pitch
            try:
                header = image.get_header()
                ((xrot, yrot),
                 (cdelt1, cdelt2)) = wcs.get_xy_rotation_and_scale(header)

                starsize = self.iqcalc.starsize(qs.fwhm_x, cdelt1,
                                                qs.fwhm_y, cdelt2)
            except Exception as e:
                self.logger.warning("Couldn't calculate star size: %s" % (str(e)))
                starsize = 0.0

            rpt_x = x + self.pixel_coords_offset
            rpt_y = y + self.pixel_coords_offset

            # make a report in the form of a dictionary
            d.setvals(x = rpt_x, y = rpt_y,
                      ra_deg = ra_deg, dec_deg = dec_deg,
                      ra_txt = ra_txt, dec_txt = dec_txt,
                      equinox = equinox,
                      fwhm = qs.fwhm,
                      fwhm_x = qs.fwhm_x, fwhm_y = qs.fwhm_y,
                      ellipse = qs.elipse, background = qs.background,
                      skylevel = qs.skylevel, brightness = qs.brightness,
                      starsize = starsize,
                      time_local = time.strftime("%Y-%m-%d %H:%M:%S",
                                                 time.localtime()),
                      time_ut = time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.gmtime()),
                      )
        except Exception as e:
            self.logger.error("Error making report: %s" % (str(e)))

        return d

    def prepare_mosaic(self, image, fov_deg, name=None, skew_limit=0.1):
        """Prepare a new (blank) mosaic image based on the pointing of
        the parameter image
        """
        header = image.get_header()
        ra_deg, dec_deg = header['CRVAL1'], header['CRVAL2']

        data_np = image.get_data()
        #dtype = data_np.dtype
        dtype = None

        # handle skew (differing rotation for each axis)?
        (rot_deg, cdelt1, cdelt2) = wcs.get_rotation_and_scale(header,
                                                               skew_threshold=skew_limit)
        self.logger.debug("image0 rot=%f cdelt1=%f cdelt2=%f" % (
            rot_deg, cdelt1, cdelt2))

        # TODO: handle differing pixel scale for each axis?
        px_scale = math.fabs(cdelt1)
        cdbase = [numpy.sign(cdelt1), numpy.sign(cdelt2)]

        self.logger.debug("creating blank image to hold mosaic")

        mosaic_img = dp.create_blank_image(ra_deg, dec_deg,
                                           fov_deg, px_scale,
                                           rot_deg,
                                           cdbase=cdbase,
                                           logger=self.logger,
                                           pfx='mosaic',
                                           dtype=dtype)

        if name is not None:
            mosaic_img.set(name=name)
        imname = mosaic_img.get('name', image.get('name', "NoName"))

        # avoid making a thumbnail of this
        mosaic_img.set(nothumb=True, path=None)

        header = mosaic_img.get_header()
        (rot, cdelt1, cdelt2) = wcs.get_rotation_and_scale(header,
                                                           skew_threshold=skew_limit)
        self.logger.debug("mosaic rot=%f cdelt1=%f cdelt2=%f" % (
            rot, cdelt1, cdelt2))

        mosaic_img.set(nothumb=True)

        return mosaic_img

    def ingest_images(self, images, mosaic_img, merge=False,
                      allow_expand=True, expand_pad_deg=0.010):

        self.logger.debug("ingesting images")
        mosaic_img.mosaic_inline(images,
                                 bg_ref=None,
                                 trim_px=None,
                                 update_minmax=False,
                                 merge=merge,
                                 allow_expand=allow_expand,
                                 expand_pad_deg=expand_pad_deg,
                                 suppress_callback=True)
        self.logger.debug("images digested")


    def load_flat(self, ccd_id, filter_name):
        self.logger.info("loading flat ccd_id=%d filter='%s'" % (
            ccd_id, filter_name))
        flat_file = os.path.join(self.flat_dir, filter_name,
                                 "FLAT-%03d.fits[1]" % ccd_id)
        self.log("attempting to load flat '%s'" % (flat_file))
        image = AstroImage.AstroImage(logger=self.logger)
        image.load_file(flat_file, memmap=False)

        data_np = image.get_data()

        # Adjust for how superflats are standardized in storage
        # (channels L-R)
        if hsc_ccd_data[ccd_id].swapxy:
            data_np = data_np.swapaxes(0, 1)
        if hsc_ccd_data[ccd_id].flipv:
            data_np = numpy.flipud(data_np)
        if hsc_ccd_data[ccd_id].fliph:
            data_np = numpy.fliplr(data_np)

        self.flat[ccd_id] = data_np

    def preprocess(self, image, dr):
        filter_name = image.get_keyword('FILTER01').strip().upper()
        ccd_id = int(image.get_keyword('DET-ID'))

        dr.remove_overscan(image, sub_bias=self.sub_bias)

        if self.use_flat:
            # flat field this piece, if flat provided
            if filter_name != self.flat_filter:
                self.log("Change of filter detected--resetting flats")
                self.flat = {}
                self.flat_filter = filter_name

            try:
                if not ccd_id in self.flat:
                    self.load_flat(ccd_id, filter_name)

                flat = self.flat[ccd_id]

                data_np = image.get_data()
                if data_np.shape == flat.shape:
                    data_np /= flat

                else:
                    raise ValueError("flat for CCD %d shape %s does not match image CCD shape %s" % (ccd_id, flat.shape, data_np.shape))

                header = {}
                image = dp.make_image(data_np, image, header)

            except Exception as e:
                self.logger.warning("Error applying flat field: %s" % (str(e)))

        return image

    def mosaic_some(self, paths, mosaic_img, dr=None, merge=False):
        images = []
        #self.log("paths are %s" % (str(paths)))
        for path in paths:
            self.logger.info("reading %s ..." % (path))
            dirname, filename = os.path.split(path)
            self.log("reading %s ..." % (filename))

            image = AstroImage.AstroImage(logger=self.logger)
            image.load_file(path, memmap=False)

            if dr is not None:
                image = self.preprocess(image, dr)
            images.append(image)

        self.ingest_images(images, mosaic_img, merge=merge)

        num_groups, self.num_groups = self.num_groups, self.num_groups-1
        ## if num_groups == 1:
        ##     self._update_gui(0, mosaic_img, self.total_files, self.start_time)

    def __update_gui(self, res, mosaic_img, total_files, start_time):
        self.fv.gui_do(self._update_gui, res, mosaic_img, total_files,
                       start_time)

    def _update_gui(self, res, mosaic_img, total_files, start_time):
        end_time = time.time()
        elapsed = end_time - start_time
        self.log("mosaiced %d files in %.3f sec" % (
            total_files, elapsed))
        imname = mosaic_img.get('name', 'mosaic')
        #self.fv.gui_do(mosaic_img.make_callback, 'modified')
        self._view.set_image(mosaic_img)
        self.log("done mosaicing")

    def mosaic(self, paths, mosaic_img, name='mosaic', fov_deg=0.2,
               num_threads=6, dr=None, merge=False):

        self.total_files = len(paths)
        if self.total_files == 0:
            return

        ingest_count = 0
        self.start_time = time.time()

        groups = dp.split_n(paths, num_threads)
        self.num_groups = len(groups)
        self.logger.info("len groups=%d" % (self.num_groups))
        ## tasks = []
        for group in groups:
            ## self.fv.nongui_do(self.mosaic_some, group, mosaic_img,
            ##                   dr=dr, merge=merge)
            ## tasks.append(Task.FuncTask(self.mosaic_some, (group, mosaic_img),
            ##                            dict(dr=dr, merge=merge),
            ##                            logger=self.logger))
            self.mosaic_some(group, mosaic_img, dr=dr, merge=merge)
        ## t = Task.ConcurrentAndTaskset(tasks)

        ## t.register_callback(self.__update_gui, args=[mosaic_img,
        ##                                              self.total_files,
        ##                                              self.start_time])
        ## t.init_and_start(self.fv)
        self._update_gui(0, mosaic_img, self.total_files, self.start_time)

def main(options, args):

    logger = log.get_logger("example2", options=options)

    if options.use_opencv:
        from ginga import trcalc
        try:
            trcalc.use('opencv')
        except Exception as e:
            logger.warning("Error using opencv: %s" % str(e))

    base_url = "http://%s:%d/app" % (options.host, options.port)

    # Create and start thread pool
    ev_quit = threading.Event()
    thread_pool = Task.ThreadPool(options.numthreads, logger,
                                  ev_quit=ev_quit)
    thread_pool.startall()

    # establish our widget application
    app = Widgets.Application(logger=logger,
                              host=options.host, port=options.port)

    #  create top level window
    window = app.make_window("gview")

    # our own viewer object, customized with methods (see above)
    viewer = GView(logger, window, thread_pool)
    viewer.set_data_dir(options.datadir)
    if options.flatdir is not None:
        viewer.set_flat_dir(options.flatdir)
    #server.add_callback('shutdown', viewer.quit)

    #window.resize(700, 540)

    if len(args) > 0:
        viewer.load_file(args[0])

    #window.show()
    #window.raise_()

    try:
        app.start()

    except KeyboardInterrupt:
        logger.info("Terminating viewer...")
        ev_quit.set()
        window.close()

if __name__ == "__main__":

    # Parse command line options with nifty optparse module
    from optparse import OptionParser

    usage = "usage: %prog [options] cmd [args]"
    optprs = OptionParser(usage=usage, version=('%%prog'))

    optprs.add_option("--debug", dest="debug", default=False, action="store_true",
                      help="Enter the pdb debugger on main()")
    optprs.add_option("-d", "--datadir", dest="datadir", metavar="DIR",
                      default='.', help="Data is in DIR")
    optprs.add_option("-f", "--flatdir", dest="flatdir", metavar="DIR",
                      help="Flats data is in DIR")
    optprs.add_option("--host", dest="host", metavar="HOST",
                      default='localhost',
                      help="Listen on HOST for connections")
    optprs.add_option("--log", dest="logfile", metavar="FILE",
                      help="Write logging output to FILE")
    optprs.add_option("--loglevel", dest="loglevel", metavar="LEVEL",
                      type='int', default=logging.INFO,
                      help="Set logging level to LEVEL")
    optprs.add_option("--numthreads", dest="numthreads", type="int",
                      default=10, metavar="NUM",
                      help="Start NUM threads in thread pool")
    optprs.add_option("--opencv", dest="use_opencv", default=False,
                      action="store_true",
                      help="Use OpenCv acceleration")
    optprs.add_option("--port", dest="port", metavar="PORT",
                      type=int, default=9909,
                      help="Listen on PORT for connections")
    optprs.add_option("--profile", dest="profile", action="store_true",
                      default=False,
                      help="Run the profiler on main()")
    optprs.add_option("--stderr", dest="logstderr", default=False,
                      action="store_true",
                      help="Copy logging also to stderr")
    optprs.add_option("-t", "--toolkit", dest="toolkit", metavar="NAME",
                      default='qt',
                      help="Choose GUI toolkit (gtk|qt)")

    (options, args) = optprs.parse_args(sys.argv[1:])

    # Are we debugging this?
    if options.debug:
        import pdb

        pdb.run('main(options, args)')

    # Are we profiling this?
    elif options.profile:
        import profile

        print(("%s profile:" % sys.argv[0]))
        profile.run('main(options, args)')


    else:
        main(options, args)

# END
