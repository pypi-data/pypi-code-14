#
# writer.py
#
# Copyright (c) 2016 Junpei Kawamoto
#
# This file is part of rgmining-common.
#
# rgmining-common is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-common is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
"""Provides writers to output information in certain format.
"""
import csv
import json


class JSONWriter(object):
    """Output reviewers in JSON format.
    """

    def __init__(self, output):
        self.output = output

    def write(self, item):
        json.dump(item, self.output)
        self.output.write("\n")


class CSVWriter(object):
    """Output reviewers in CSV format.
    """

    def __init__(self, output, headers):
        self.output = csv.DictWriter(output, headers)
        self.output.writeheader()

    def write(self, item):
        self.output.writerow(item)
