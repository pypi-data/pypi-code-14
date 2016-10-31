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

from os.path import join, dirname, isfile, isdir

RESOURCES_DIRECTORY_PATH = "/usr/share/lento_dvd"

# when running vgapplet directly from sources - use resources from source code
__RELATIVE_RESOURCE_PATH = join(dirname(dirname(__file__)))

if isfile(join(__RELATIVE_RESOURCE_PATH, "bin", "lento_dvd")):
    # Running directly from source
    __CURRENT_RESOURCES_PATH = __RELATIVE_RESOURCE_PATH
elif isdir(join(__RELATIVE_RESOURCE_PATH, "usr", "share", "lento_dvd")):
    # Installed as user (~/.local/...)
    __CURRENT_RESOURCES_PATH = join(__RELATIVE_RESOURCE_PATH, "usr", "share", "lento_dvd")
else:
    # Installed globally (/usr/share)
    __CURRENT_RESOURCES_PATH = RESOURCES_DIRECTORY_PATH


def image_path(name):
    """Returns path to the image file by its name"""
    return join(__CURRENT_RESOURCES_PATH, "img", "%s.svg" % name)
