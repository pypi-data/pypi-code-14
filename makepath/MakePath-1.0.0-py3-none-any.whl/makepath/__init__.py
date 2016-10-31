#
#   Copyright 2016 Olivier Kozak
#
#   This file is part of MakePath.
#
#   MakePath is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
#   version.
#
#   MakePath is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
#   details.
#
#   You should have received a copy of the GNU Lesser General Public License along with MakePath. If not, see
#   <http://www.gnu.org/licenses/>.
#

import os
import traceback


def from_root(path, *paths):
    return os.path.join(os.path.sep, path, *paths)


def from_home(path, *paths):
    return os.path.join(os.path.expanduser("~"), path, *paths)


def from_working_dir(path, *paths):
    return os.path.abspath(os.path.join(path, *paths))


def from_this_file(path, *paths):
    for item in reversed(traceback.extract_stack()):
        if item.filename != os.path.abspath(__file__):
            break

    # noinspection PyUnboundLocalVariable
    return os.path.abspath(os.path.join(os.path.relpath(os.path.dirname(item.filename)), path, *paths))
