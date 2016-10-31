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

import os
from distutils.core import setup

from lento_dvd.resource import RESOURCES_DIRECTORY_PATH


def find_resources(resource_dir):
    target_path = os.path.join(RESOURCES_DIRECTORY_PATH, resource_dir)
    resource_names = os.listdir(resource_dir)
    resource_list = [os.path.join(resource_dir, file_name) for file_name in resource_names]
    return (target_path, resource_list)


setup(name="lento_dvd",
      version="0.1.0",
      description="LentoDVD Speed Limiter",
      url='https://github.com/sneakypete81/lento_dvd',
      author='Pete Burgers',
      author_email='sneakypete81@gmail.com',
      license='GPL',
      packages=["lento_dvd"],
      data_files=[
          ('/usr/share/applications', ['lento_dvd.desktop']),
          find_resources("img")],
      scripts=["bin/lento_dvd"]
)
