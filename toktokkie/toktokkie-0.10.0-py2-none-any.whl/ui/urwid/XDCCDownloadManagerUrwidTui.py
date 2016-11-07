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
from __future__ import division
from __future__ import absolute_import
import os
import time
import urwid
from threading import Thread
from xdcc_dl.entities.Progress import Progress
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher
from xdcc_dl.xdcc.MultipleServerDownloader import MultipleServerDownloader
from toktokkie.utils.iconizing.Iconizer import Iconizer
from toktokkie.utils.renaming.schemes.SchemeManager import SchemeManager
from toktokkie.utils.xdcc.XDCCDownloadManager import XDCCDownloadManager
from toktokkie.utils.iconizing.procedures.ProcedureManager import ProcedureManager
from itertools import ifilter


class XDCCDownloadManagerUrwidTui(object):
    u"""
    Urwid TUI for the XDCC Download Manager functionality
    """

    def __init__(self):
        u"""
        Initializes the TUI's various widgets
        """

        self.searching = False
        self.downloading = False

        self.upper_body = []
        self.middle_body = []
        self.lower_body = []

        self.loop = None
        self.top = None
        self.list_walker = None

        self.title = urwid.Text(u"XDCC Download Manager")
        self.target_directory_edit = urwid.Edit(u"Target Directory:")
        self.target_directory_edit.set_edit_text(os.getcwdu())
        self.series_name_edit = urwid.Edit(u"Series Name:")
        self.season_number_edit = urwid.Edit(u"Season Number:")
        self.episode_number_edit = urwid.Edit(u"Episode Number:")

        self.renaming_schemes = []
        for scheme in SchemeManager.get_scheme_names():
            urwid.RadioButton(self.renaming_schemes, scheme)
        self.rename_check = urwid.CheckBox(u"Auto-rename", state=True)

        self.iconizing_procedures = []
        for procedure in ProcedureManager.get_procedure_names():
            urwid.RadioButton(self.iconizing_procedures, procedure)
        self.iconize_check = urwid.CheckBox(u"Iconize", state=True)

        self.search_term_edit = urwid.Edit(u"Search Term:")
        self.search_engines = []
        for engine in [u"All"] + PackSearcher.get_available_pack_searchers():
            urwid.RadioButton(self.search_engines, engine)

        self.search_button = urwid.Button(u"Search")

        self.search_results = []
        self.search_result_checks = []

        self.download_button = urwid.Button(u"Download")

        self.single_progress_bar = urwid.ProgressBar(u"Single N", u"Single C")
        self.total_progress_bar = urwid.ProgressBar(u"Total N", u"Total N")
        self.current_speed = urwid.Text(u"Current Speed:")
        self.average_speed = urwid.Text(u"Average Speed:")

        self.lay_out()
        self.connect_widgets()

    def lay_out(self):
        u"""
        Handles the layout of the TUI elements

        :return: None
        """
        div = urwid.Divider()

        self.upper_body = [self.title, div, self.target_directory_edit, self.series_name_edit, self.season_number_edit]
        self.upper_body += [self.episode_number_edit, div] + self.renaming_schemes + [self.rename_check, div]
        self.upper_body += self.iconizing_procedures + [self.iconize_check, div]
        self.upper_body += [self.search_term_edit] + self.search_engines + [self.search_button, div]

        self.lower_body = [div, self.download_button, div, self.single_progress_bar, self.total_progress_bar]
        self.lower_body += [self.current_speed, self.average_speed]

        body = self.upper_body + self.middle_body + self.lower_body

        self.list_walker = urwid.SimpleFocusListWalker(body)
        self.top = urwid.Overlay(urwid.Padding(urwid.ListBox(self.list_walker), left=2, right=2),
                                 urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                                 align=u'center', width=(u'relative', 80),
                                 valign=u'middle', height=(u'relative', 70),
                                 min_width=20, min_height=10)

    def update_layout(self):
        u"""
        Updates the layout of the TUI Widgets

        :return: None
        """
        self.search_result_checks = []

        for result in self.search_results:
            self.search_result_checks.append(urwid.CheckBox(result.get_filename()))

        self.middle_body = self.search_result_checks
        self.list_walker[:] = self.upper_body + self.middle_body + self.lower_body
        self.loop.draw_screen()

    def connect_widgets(self):
        u"""
        Connects the various widgets to their functionality

        :return: None
        """
        urwid.connect_signal(self.target_directory_edit, u'change', self.parse_directory)
        urwid.connect_signal(self.search_button, u'click', self.start_search)
        urwid.connect_signal(self.download_button, u'click', self.start_download)

    def start(self):
        u"""
        Starts the TUI

        :return: None
        """
        self.loop = urwid.MainLoop(self.top, palette=[(u'reversed', u'standout', u'')])
        self.loop.run()

    # noinspection PyUnusedLocal
    def parse_directory(self, widget, directory):
        u"""
        Parses the currently entered directory, and fills in the information it can gather from that into the
        relevant UI elements

        :param widget:    The widget that did the method call
        :param directory: The new content of the widget's edit text
        :return:          None
        """
        series_name = os.path.basename(directory)
        season, episode = XDCCDownloadManager.get_max_season_and_episode_number(directory)

        self.series_name_edit.set_edit_text(series_name)
        self.search_term_edit.set_edit_text(series_name)
        self.episode_number_edit.set_edit_text(unicode(episode))
        self.season_number_edit.set_edit_text(unicode(season))

    # noinspection PyUnusedLocal
    def start_search(self, widget):
        u"""
        Starts searching for the XDCC pack specified via the search term and search engines to use

        :param widget: The widget that called this method
        :return:       None
        """
        if self.searching:
            return

        def search():

            self.searching = True

            search_term = self.search_term_edit.get_edit_text()
            search_engine = list(ifilter(lambda x: x.get_state(), self.search_engines))[0].get_label()

            if search_engine == u"All":
                self.search_results = PackSearcher(PackSearcher.get_available_pack_searchers()).search(search_term)
            else:
                self.search_results = PackSearcher([search_engine]).search(search_term)

            self.update_layout()
            self.searching = False

        Thread(target=search).start()
        Thread(target=self.spinner).start()

    # noinspection PyUnusedLocal
    def start_download(self, widget):
        u"""
        Starts the XDCC download procedure

        :param widget: The widget that called this method
        :return:       None
        """
        if self.downloading or self.searching:
            return

        try:
            season = int(self.season_number_edit.get_edit_text())
            episode = int(self.episode_number_edit.get_edit_text())
        except ValueError:
            return

        destination_directory, season_directory = \
            XDCCDownloadManager.prepare_directory(self.target_directory_edit.get_edit_text(),
                                                  self.series_name_edit.get_edit_text(),
                                                  season)

        selected_packs = []
        for i, result in enumerate(self.search_result_checks):
            if result.get_state():
                selected_packs.append(self.search_results[i])

        for i, pack in enumerate(selected_packs):
            name = u"xdcc_dl_" + unicode(i).zfill(int(len(selected_packs) / 10) + 1)
            pack.set_directory(season_directory)
            pack.set_filename(name, override=True)

        # noinspection PyShadowingNames
        progress = Progress(len(selected_packs), callback=self.progress_update)

        def handle_download():

            self.downloading = True
            MultipleServerDownloader(u"random").download(selected_packs, progress)

            if self.rename_check.get_state():
                scheme = SchemeManager.get_scheme_from_scheme_name(
                    list(ifilter(lambda x: x.get_state(), self.renaming_schemes))[0].get_label())

                XDCCDownloadManager.auto_rename(scheme, episode, selected_packs)

            if self.iconize_check.get_state():
                iconization_method = list(ifilter(lambda x: x.get_state(), self.iconizing_procedures))[0].get_label()
                Iconizer(iconization_method).iconize_directory(destination_directory)

            self.downloading = False
            self.progress_update(0, 0, 0.0, 0, 0, 0.0, 0, 0)
            self.current_speed.set_text(u"Current Speed:")
            self.average_speed.set_text(u"Average Speed:")

        Thread(target=handle_download).start()
        Thread(target=self.spinner).start()

    def spinner(self, delay = 0.5):
        u"""
        Animates the search and download buttons whenever a search or download is running

        :param delay: The delay between animation steps
        :return:      None
        """

        while self.downloading or self.searching:

            def dots(x):
                return ((x.count(u".") % 3) + 1) * u"."

            if self.downloading:
                self.download_button.set_label(u"Downloading" + dots(self.download_button.get_label()))
            else:
                self.download_button.set_label(u"Download")

            if self.searching:
                self.search_button.set_label(u"Searching" + dots(self.search_button.get_label()))
            else:
                self.search_button.set_label(u"Search")

            self.loop.draw_screen()
            time.sleep(delay)

        self.download_button.set_label(u"Download")
        self.search_button.set_label(u"Search")
        self.loop.draw_screen()

    # noinspection PyUnusedLocal
    def progress_update(self, single_progress, single_total, single_percentage,
                        total_progress, total_total, total_percentage,
                        current_speed, average_speed):
        u"""
        Updates the TUI's progress widgets

        :param single_progress:    The Single Progress
        :param single_total:       The Single Total Size
        :param single_percentage:  The Single Completion Percentage
        :param total_progress:     The Total Progress
        :param total_total:        The Total Size
        :param total_percentage:   The Total Completion Percentage
        :param current_speed:      The current speed in Byte/s
        :param average_speed:      The average speed in Byte/s
        :return:                   None
        """
        self.single_progress_bar.set_completion(int(single_percentage))
        self.total_progress_bar.set_completion(int(total_percentage))
        self.current_speed.set_text(u"Current Speed: " + unicode(int(current_speed / 1000)) + u" kB/s")
        self.average_speed.set_text(u"Average Speed: " + unicode(int(average_speed / 1000)) + u" kB/s")
        self.loop.draw_screen()
