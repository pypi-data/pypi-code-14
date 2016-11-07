u"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
import os
import urwid
from toktokkie.utils.iconizing.Iconizer import Iconizer


class FolderIconizerUrwidTui(object):
    u"""
    Urwid TUI for the Directory Iconizing functionality
    """

    def __init__(self):
        u"""
        Initializes the TUI's various widgets
        """
        self.iconizer = Iconizer()

        self.top = None
        self.list_walker = None

        self.title = urwid.Text(u"Folder Iconizer")

        self.directory_text = urwid.Text(u"Directory:")
        self.directory_edit = urwid.Edit()
        self.directory_edit.set_edit_text(os.getcwdu())

        self.recursive_check = urwid.CheckBox(u"Recursive?")

        self.iconize_button = urwid.Button(u"Iconize")
        urwid.connect_signal(self.iconize_button, u'click', self.iconize)

        self.lay_out()

    def lay_out(self):
        u"""
        Handles the layout of the TUI elements

        :return: None
        """
        div = urwid.Divider()

        directory_edit = urwid.AttrMap(self.directory_edit, None, focus_map=u'reversed')
        iconize_button = urwid.AttrMap(self.iconize_button, None, focus_map=u'reversed')

        body = [self.title, div, self.directory_text, directory_edit, div, self.recursive_check, div, iconize_button]

        self.list_walker = urwid.SimpleFocusListWalker(body)
        self.top = urwid.Overlay(urwid.Padding(urwid.ListBox(self.list_walker), left=2, right=2),
                                 urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                                 align=u'center', width=(u'relative', 80),
                                 valign=u'middle', height=(u'relative', 70),
                                 min_width=20, min_height=10)

    def start(self):
        u"""
        Starts the TUI

        :return: None
        """
        urwid.MainLoop(self.top, palette=[(u'reversed', u'standout', u'')]).run()

    # noinspection PyUnusedLocal
    def iconize(self, iconize_button, parameters = None):
        u"""
        Starts the iconization

        :param iconize_button: The button that called this method
        :param parameters:     The parameters given, will not be used
        :return:               None
        """
        directory = self.directory_edit.get_edit_text()

        if self.recursive_check.get_state():
            self.iconizer.recursive_iconize(directory)
        else:
            self.iconizer.iconize_directory(directory)
