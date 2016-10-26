u"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of xdcc_dl.

    xdcc_dl is a program that allows downloading files via hte XDCC
    protocol via file serving bots on IRC networks.

    xdcc_dl is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    xdcc_dl is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with xdcc_dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
import os
import time
import struct
import irc.client
# noinspection PyPep8Naming
from xdcc_dl.logging.LoggingTypes import LoggingTypes as LOG
from xdcc_dl.xdcc.layers.xdcc.XDCCInitiator import XDCCInitiator


class IncompleteDownload(Exception):
    u"""
    Exception raised whenever a DCC connection was ended, but the file was not completed.
    """
    pass


# noinspection PyUnusedLocal
class DownloadHandler(XDCCInitiator):
    u"""
    Class that handles the download process
    Layer 5 of the XDCC Bot
    """

    def on_dccmsg(self, connection, event):
        u"""
        Runs each time a new chunk of data is received while downloading

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        data = event.arguments[0]
        data_length = len(data)

        self.file.write(data)
        self.progress.add_single_progress(data_length)

        progress_message = u" Progress: %.2f" % self.progress.get_single_progress_percentage()
        progress_message += u"% (" + unicode(self.progress.get_single_progress())
        progress_message += u"/" + unicode(self.progress.get_single_progress_total()) + u")"

        self.logger.log(progress_message, LOG.DOWNLOAD_PROGRESS, carriage_return=True)

        # Send Acknowledge Message
        self.dcc_connection.send_bytes(struct.pack(u"!I", self.progress.get_single_progress()))
        # -> on_dccmsg if download not yet complete
        # -> on_dcc_disconnect if completed

    def on_dcc_disconnect(self, connection, event):
        u"""
        The DCC Connection was disconnected. Checks if download was completed. If not, try to resend Pack request

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.file.close()
        self.logger.log(u"\nDownload completed in %.2f seconds" % (time.time() - self.start_time))

        if os.path.getsize(self.current_pack.get_filepath()) < self.filesize:
            raise IncompleteDownload()

        self.connection.close()
        self.connection.disconnect()  # -> on_diconnect
