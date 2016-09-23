# vi:et:ts=4 sw=4 sts=4
#
# local-pipelines : run Bitbucket pipelines locally
# Copyright (C) 2016  Gary Kramlich <grim@reaperworld.com>
# Copyright (C) 2016  Sean Farley <sean@farley.io>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import os
import stat
import tempfile


class Step(object):
    def __init__(self, image, script):
        self._image = image

        self._script = ["#!/bin/bash", "set -ex"]
        if script is not None:
            self._script.extend(script)

    @classmethod
    def from_dict(cls, dict):
        image = dict.get("image", None)
        script = dict.get("script", [])

        return cls(image, script)

    @property
    def image(self):
        return self._image

    @property
    def script(self):
        return self._script

    def __str__(self):
        return "\n".join(self._script)

    def script_file(self):
        fd, filename = tempfile.mkstemp(
            prefix=".pipeline-",
            suffix=".sh",
            dir=os.getcwd(),
        )
        filename = os.path.realpath(filename)

        with os.fdopen(fd, "w") as ofp:
            ofp.write(str(self))

        # now set the executebit
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC)

        return filename
