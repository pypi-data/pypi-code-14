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
import sys
from subprocess import Popen, check_output
from toktokkie.utils.iconizing.procedures.GenericProcedure import GenericProcedure


class GnomeProcedure(GenericProcedure):
    """
    Iconizing Procedure used on Linux system using Gnome and Gnome-derivative desktop environments
    """

    @staticmethod
    def is_applicable() -> bool:
        """
        The Gnome procedure is applicable if the system is running Linux as well as a Gnome environment,
        like the Gnome DE or Cinnamon

        :return: True, if the procedures is applicable, False otherwise
        """
        try:
            return sys.platform == "linux" and os.environ["DESKTOP_SESSION"] in ["cinnamon", "gnome"]
        except KeyError:
            return False

    @staticmethod
    def iconize(directory: str, icon_file: str) -> None:
        """
        Iconizes the given directory using gvfs and the provided icon file
        The icon file should be a PNG file
        The file extension may be omiited, i.e. icon instead of icon.png

        :param directory: The directory to iconize
        :param icon_file: The icon file to use.
        :return:          None
        """
        if not icon_file.endswith(".png"):
            icon_file += ".png"

        Popen(["gvfs-set-attribute", "-t", "string", directory, "metadata::custom-icon", "file://" + icon_file]).wait()

    @staticmethod
    def reset_iconization_state(directory: str) -> None:
        """
        Resets the iconization state of the given directory using the unset option of gvfs-set-attribute
        :param directory: the directory to de-iconize
        :return:          None
        """
        Popen(["gvfs-set-attribute", "-t", "unset", directory, "metadata::custom-icon"]).wait()

    @staticmethod
    def get_icon_file(directory: str) -> str or None:
        """
        Returns the path to the given directory's icon file, if it is iconized. If not, None is returned

        :param directory: The directory to check
        :return:          Either the path to the icon file or None if no icon file exists
        """
        gvfs_info = check_output(["gvfs-info", directory]).decode()

        if "metadata::custom-icon: file://" in gvfs_info:
            return gvfs_info.split("metadata::custom-icon: file://")[1].split("\n")[0]
        else:
            return None

    @staticmethod
    def get_procedure_name() -> str:
        """
        :return: The name of the Procedure
        """
        return "gnome"
