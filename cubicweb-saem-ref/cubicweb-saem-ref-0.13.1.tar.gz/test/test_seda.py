# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as publishged by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-saem-ref tests for SEDA cube integration"""

import unittest

from cubicweb import devtools  # noqa
from cubes.saem_ref.entities import seda  # noqa - trigger monkey-patch
from cubes.seda.entities.profile_generation import SEDA1XSDExport


class CWURIURLTC(unittest.TestCase):

    def test(self):

        class FakeEntity(object):
            def __init__(self, cwuri):
                self.cwuri = cwuri
                self._cw = self

            def build_url(self, uri):
                return 'http://thistest/' + uri

        self.assertEqual(SEDA1XSDExport.cwuri_url(FakeEntity('ark:12/3')),
                         'http://thistest/ark:12/3')
        self.assertEqual(SEDA1XSDExport.cwuri_url(FakeEntity('http://othertest/ark:12/3')),
                         'http://othertest/ark:12/3')
        self.assertEqual(SEDA1XSDExport.cwuri_url(FakeEntity('http://othertest/whatever')),
                         'http://othertest/whatever')
        self.assertEqual(SEDA1XSDExport.cwuri_url(FakeEntity('whatever')),
                         'whatever')


if __name__ == '__main__':
    unittest.main()
