"""
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
import os
import urwid
from toktokkie.utils.renaming.TVSeriesRenamer import TVSeriesRenamer
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager


class TVSeriesRenamerUrwidTui(object):
    """
    Urwid TUI for the TV Series Renamer functionality
    """

    def __init__(self) -> None:
        """
        Initializes the TUI's various widgets
        """

        self.renamer = None
        self.confirmation = None

        self.list_walker = None
        self.upper_body, self.middle_body, self.lower_body = [[], [], []]
        self.top = None

        self.title = urwid.Text("TV Episode Renamer")

        self.naming_scheme_text = urwid.Text("Naming Scheme:")
        self.renaming_schemes = []

        for scheme in SchemeManager.get_scheme_names() + ["Test"]:
            urwid.RadioButton(group=self.renaming_schemes, label=scheme)

        self.dir_entry_text = urwid.Text("Directory:")
        self.dir_entry = urwid.Edit()
        self.dir_entry.set_edit_text(os.getcwd())
        self.recursive_check = urwid.CheckBox("Recursive?")
        self.start_search_button = urwid.Button("Start Search")
        urwid.connect_signal(self.start_search_button, 'click', self.search)

        self.episodes_text = urwid.Text("Episodes: (Old -> New)")

        self.confirm_button = urwid.Button("Confirm")
        urwid.connect_signal(self.confirm_button, 'click', self.confirm)

        self.lay_out()

    def lay_out(self) -> None:
        """
        Handles the layout of the TUI elements

        :return: None
        """
        div = urwid.Divider()

        self.confirm_button = urwid.AttrMap(self.confirm_button, None, focus_map='reversed')
        self.start_search_button = urwid.AttrMap(self.start_search_button, None, focus_map='reversed')

        dir_entry_formatted = urwid.AttrMap(self.dir_entry, None, focus_map='reversed')

        self.upper_body = [self.title, div, self.naming_scheme_text] + self.renaming_schemes + [div]
        self.upper_body += [self.dir_entry_text, dir_entry_formatted, self.recursive_check, self.start_search_button]
        self.upper_body += [div, self.episodes_text, div]
        self.lower_body = [div, self.confirm_button]

        self.list_walker = urwid.SimpleFocusListWalker(self.upper_body + self.middle_body + self.lower_body)
        self.top = urwid.Overlay(urwid.Padding(urwid.ListBox(self.list_walker), left=2, right=2),
                                 urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                                 align='center', width=('relative', 80),
                                 valign='middle', height=('relative', 70),
                                 min_width=20, min_height=10)

    def start(self) -> None:
        """
        Starts the TUI

        :return: None
        """
        urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')]).run()

    # noinspection PyUnusedLocal
    def confirm(self, button: urwid.Button) -> None:
        """
        Starts the renaming process

        :param button: The Confirm Button
        :return:       None
        """
        if self.confirmation is not None and self.renamer is not None:
            for index, confirmation in enumerate(self.confirmation):
                if self.middle_body[index].get_state():
                    confirmation.confirm()

        self.renamer.confirm(self.confirmation)
        self.renamer.start_rename()

        # noinspection PyTypeChecker
        self.search(None)

    # noinspection PyUnusedLocal
    def search(self, directory_entry: urwid.Button, parameters: None = None) -> None:
        """
        Fills the episode list from the provided directory with the current recursive option

        :param directory_entry: The widget that caused the method to be called
        :param parameters:      Parameters passed by the widget, but not used
        :return:                None
        """
        directory = self.dir_entry.get_edit_text()
        self.renamer = None
        self.confirmation = None

        if os.path.isdir:

            recursive = self.recursive_check.get_state()
            scheme = ""
            for radio_button in self.renaming_schemes:
                if radio_button.get_state():
                    scheme = radio_button.get_label()

            self.renamer = TVSeriesRenamer(directory, SchemeManager.get_scheme_from_scheme_name(scheme), recursive)
            self.confirmation = self.renamer.request_confirmation()

        self.refresh()

    def refresh(self) -> None:
        """
        Refreshes the Window with the currently active widgets

        :return: None
        """
        self.middle_body = []

        if self.confirmation is not None:

            old_name_max = max(len(x.get_names()[0]) for x in self.confirmation) + 1

            for episode in self.confirmation:
                episode_checkbox = urwid.CheckBox(
                    episode.get_names()[0].ljust(old_name_max) + " --->  " + episode.get_names()[1])
                episode_checkbox.set_state(True)
                self.middle_body.append(episode_checkbox)

        self.list_walker[:] = self.upper_body + self.middle_body + self.lower_body
