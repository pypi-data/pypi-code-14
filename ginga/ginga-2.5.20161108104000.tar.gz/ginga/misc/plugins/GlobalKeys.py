#
# GlobalKeys.py -- Non-channel specific key bindings plugin for Ginga viewer
#
# Eric Jeschke (eric@naoj.org)
#
# Copyright (c) Eric R. Jeschke.  All rights reserved.
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
import platform
import numpy

from ginga import GingaPlugin
from ginga.misc import Bunch
from ginga.gw import Widgets, Readout


class GlobalKeys(GingaPlugin.GlobalPlugin):

    def __init__(self, fv):
        # superclass defines some variables for us, like logger
        super(GlobalKeys, self).__init__(fv)

        prefs = self.fv.get_preferences()
        self.settings = prefs.createCategory('plugin_GlobalKeys')
        #self.settings.addDefaults()
        self.settings.load(onError='silent')

        fv.add_callback('add-channel', self._add_channel_cb)

        self.ds = fv.ds

    # No GUI presently
    ## def build_gui(self, container):
    ##     pass

    def keypress_cb(self, fitsimage, keyname, channel):
        """Key press event in a channel window."""
        chname = channel.name
        self.logger.debug("key press (%s) in channel %s" % (
            keyname, chname))
        # TODO: keyboard accelerators to raise tabs need to be integrated into
        #   the desktop object
        if keyname == 'Z':
            self.ds.raise_tab('Zoom')
        ## elif keyname == 'T':
        ##     self.ds.raise_tab('Thumbs')
        elif keyname == 'I':
            self.ds.raise_tab('Info')
        elif keyname == 'H':
            self.ds.raise_tab('Header')
        elif keyname == 'C':
            self.ds.raise_tab('Contents')
        elif keyname == 'D':
            self.ds.raise_tab('Dialogs')
        # TEMP: disabled until fixed
        ## elif keyname == 'F':
        ##     self.fv.build_fullscreen()
        elif keyname == 'f':
            self.fv.toggle_fullscreen()
        elif keyname == 'm':
            self.fv.maximize()
        elif keyname == '<':
            self.fv.collapse_pane('left')
        elif keyname == '>':
            self.fv.collapse_pane('right')
        elif keyname == 'b':
            self.fv.prev_channel()
        elif keyname == 'n':
            self.fv.next_channel()
        elif keyname == 'j':
            self.fv.cycle_workspace_type()
        elif keyname == 'L':
            self.fv.add_channel_auto()
        ## elif keyname == 'escape':
        ##     self.fv.reset_viewer()
        elif keyname == 'up':
            self.fv.prev_image()
        elif keyname == 'down':
            self.fv.next_image()
        elif keyname == 'left':
            self.fv.prev_channel()
        elif keyname == 'right':
            self.fv.next_channel()
        return True

    def _add_channel_cb(self, viewer, channel):
        chname = channel.name
        fi = channel.fitsimage

        fi.add_callback('key-press', self.keypress_cb, channel)

    def start(self):
        pass

    def __str__(self):
        return 'globalkeys'

#END
