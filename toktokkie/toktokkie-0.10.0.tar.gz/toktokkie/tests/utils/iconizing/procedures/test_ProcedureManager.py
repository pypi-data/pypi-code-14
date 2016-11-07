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
import unittest
from toktokkie.utils.iconizing.procedures.ProcedureManager import ProcedureManager


class ProcedureManagerUnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_procedure_name_passing(self):
        all_procedures = ProcedureManager.get_all_procedures()
        procedure_names = ProcedureManager.get_procedure_names(supports_current_platform=False)

        for procedure in all_procedures:
            self.assertTrue(procedure.get_procedure_name() in procedure_names)
            self.assertEqual(procedure,
                             ProcedureManager.get_procedure_from_procedure_name(procedure.get_procedure_name()))
