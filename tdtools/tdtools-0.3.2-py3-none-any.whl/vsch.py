"""Python Class that represents an "evolutionary schema". Class attributes
return either table with the same name or a table expressions"""

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2016, Paresh Adhia"
__license__ = "GPL"

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class VSchema:
	def __init__(self, sch, sch_hist, version=None):
		self.sch, self.sch_hist, self._version = sch, sch_hist, version


	@property
	def version(self):
		if not self._version:
			from .sqlcsr import csr
			csr.execute("Select InfoData From DBC.DBCInfoV Where InfoKey = 'VERSION'")
			self._version = csr.fetchone()[0]

		return self._version


	def __getattr__(self,tab):
		vcols = []

		for tab_hist in self.sch_hist.get(tab,[]):
			for ver, cols in tab_hist.items():
				if ver > self.version:
					vcols.extend(cols)

		if not vcols:
			return '{}.{}'.format(self.sch,tab)

		colexpr = ', '.join(['{} AS {}'.format(v,k) for cmap in vcols for k,v in cmap.items()])
		return '(SELECT _T.*, {} FROM {}.{} AS _T)'.format(colexpr, self.sch, tab)


_dbc_schema = None
def dbc_schema():
	global _dbc_schema

	if not _dbc_schema:
		import json
		from pkg_resources import resource_filename

		with open(resource_filename(__name__,'dbc.json'),'r') as dbc_sch:
			_dbc_schema = VSchema('dbc',json.load(dbc_sch))

	return _dbc_schema
