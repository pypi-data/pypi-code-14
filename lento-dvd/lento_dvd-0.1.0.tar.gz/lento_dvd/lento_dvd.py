#!/usr/bin/python3

# Copyright 2016, Pete Burgers (https://github.com/sneakypete81)
#
# Boilerplate code adapted from Vagrant AppIndicator
# (https://github.com/candidtim/vagrant-appindicator)
# Thanks @candidtim!
#
# This file is part of LentoDVD.
#
# LentoDVD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# LentoDVD is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with LentoDVD.
# If not, see <http://www.gnu.org/licenses/>.

import signal
import subprocess

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib as glib

from . import resource
from . import eject

APPINDICATOR_ID = 'lento_dvd_appindicator'
NO_LIMIT = 0
SPEEDS = [1, 2, 4, 8, 16, 32, 64]
OVERRIDE_INTERVAL = 5

class LentoDvd(object):
    def __init__(self):
        self.indicator = appindicator.Indicator.new(
            APPINDICATOR_ID, resource.image_path("icon-off"),
            appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        self.timer = None

        self._build_menu()
        self.update(NO_LIMIT)

    def _shutdown(self):
        self.change_speed(NO_LIMIT)

    def run(self):
        gtk.main()

    def _build_menu(self):
        menu = gtk.Menu()

        title_item = gtk.MenuItem("Limit DVD Speed")
        title_item.set_sensitive(False)
        menu.append(title_item)

        no_limit_item = gtk.RadioMenuItem("No Limit")
        no_limit_item.set_active(True)
        no_limit_item.connect('activate', self.on_change_speed, NO_LIMIT)

        for speed in SPEEDS:
            speed_item = gtk.RadioMenuItem("%dx" % speed, group=no_limit_item)
            speed_item.connect('activate', self.on_change_speed, speed)
            menu.append(speed_item)

        menu.append(no_limit_item)

        menu.append(gtk.SeparatorMenuItem("Options"))

        item_about = gtk.MenuItem('Help')
        item_about.connect('activate', self.on_about)
        menu.append(item_about)

        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.on_quit)
        menu.append(item_quit)

        menu.show_all()
        self.indicator.set_menu(menu)

    def open_about_page(self):
        import webbrowser
        webbrowser.open('https://github.com/sneakypete81/lento_dvd')

    def quit(self):
        self._shutdown()
        gtk.main_quit()

    def update(self, speed):
        """
        Entry point for appindicator update.
        Triggers all UI modifications necessary on updates of DVD speed.
        """
        self._update_icon(speed)

    def change_speed(self, speed):
        self.update(speed)

        if self.timer:
            glib.source_remove(self.timer)
            self.timer = None

        try:
            eject.eject(cdspeed=speed)
        except subprocess.CalledProcessError as error:
            print(error)
            return False

        # Keep overriding the speed every 5 seconds, in case a new DVD gets inserted
        if speed != NO_LIMIT:
            self.timer = glib.timeout_add_seconds(OVERRIDE_INTERVAL,
                                                  self.change_speed, speed)

        return True

    def _update_icon(self, speed):
        """Updates main appindicator icon to reflect the DVD speed"""
        if speed == NO_LIMIT:
            icon_name = "icon-off"
        else:
            icon_name = "icon-on"

        icon = resource.image_path(icon_name)
        self.indicator.set_icon(icon)

    # UI listeners
    def on_change_speed(self, item, speed):
        # An 'activate' event is triggered when a menu item is deselected.
        # This event must be ignored.
        if item.get_active():
            self.change_speed(speed)

    def on_about(self, _):
        self.open_about_page()

    def on_quit(self, _):
        self.quit()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    LentoDvd().run()

if __name__ == "__main__":
    main()
