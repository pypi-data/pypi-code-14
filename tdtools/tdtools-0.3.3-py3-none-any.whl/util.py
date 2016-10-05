"Teradata utility functions"

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

class EnhancedCursor:
	"Cursor wrapper class with some useful attributes"

	_version = None

	def __init__(self, csr):
		self.csr = csr

	@property
	def version(self):
		if not EnhancedCursor._version:
			self.csr.execute("Select InfoData From DBC.DBCInfoV Where InfoKey = 'VERSION'")
			EnhancedCursor._version = self.csr.fetchone()[0]
		return EnhancedCursor._version

	@property
	def schema(self):
		self.execute('select database')
		return self.fetchone()[0]

	@schema.setter
	def schema(self, new_schema):
		import sqlcsr

		self.execute('database ' + new_schema)
		sqlcsr.commit()

	def fetchxml(self):
		import re

		val, rows = '', self.fetchmany(100)
		while rows:
			for row in rows:
				val += row[0]
			rows = self.fetchmany(100)

		val = re.sub('xmlns=".*?"','',re.sub('encoding="UTF-16"','encoding="utf-8"',val,1,flags=re.IGNORECASE),1)

		return val

	def __getattr__(self,attr):  return getattr(self.csr,attr)

# Classes to represent (object/database) hierarchy
class Links:
	fancy  = {'T':" ├─", 'L':" └─", 'I':" │ ", ' ':"   "}
	simple = {'T':" |-", 'L':" L_", 'I':" | ", ' ':"   "}

	style = fancy

	@staticmethod
	def set_style(style):
		Links.style = style

	def __init__(self, chain=''):
		self.chain = chain

	def extend(self,ch):
		return Links(self.chain.replace('L',' ').replace('T','I') + ch)

	def __str__(self):
		return ''.join([self.style[k] for k in self.chain])


class Node:
	def __init__(self, parent):
		self.parent, self.children = parent, []

	def tree_walk(self, pfx=Links()):
		yield (pfx,self)

		if self.children:
			for c in self.children[:-1]:
				yield from c.tree_walk(pfx.extend('T'))
			yield from self.children[-1].tree_walk(pfx.extend('L'))


def format_size(num,fmtstr='{}'):
	if   num == None   : pass
	elif num == 0      : num = '0'
	elif num % 1e9 == 0: num = fmtstr.format(int(num//1e9)) + 'e9'
	elif num % 1e6 == 0: num = fmtstr.format(int(num//1e6)) + 'e6'
	elif num % 1e3 == 0: num = fmtstr.format(int(num//1e3)) + 'e3'
	else:
		num = fmtstr.format(num)

	return num

priv_name = {
  'AE': 'Alter External Procedure'
, 'AF': 'Alter Function'
, 'AP': 'Alter Procedure'
, 'AS': 'AbortSession'
, 'CA': 'Create Authorization'
, 'CD': 'Create Database'
, 'CE': 'Create External Procedure'
, 'CF': 'Create Function'
, 'CG': 'Create Trigger'
, 'CM': 'Create Macro'
, 'CO': 'Create Profile'
, 'CP': 'Checkpoint'
, 'CR': 'Create Role'
, 'CS': 'Create Server'
, 'CT': 'Create Table'
, 'CU': 'Create User'
, 'CV': 'Create View'
, 'CZ': 'Create Zone'
, 'D ': 'Delete'
, 'DA': 'Drop Authorization'
, 'DD': 'Drop Database'
, 'DF': 'Drop Function'
, 'DG': 'Drop Trigger'
, 'DM': 'Drop Macro'
, 'DO': 'Drop Profile'
, 'DP': 'Dump'
, 'DR': 'Drop Role'
, 'DS': 'Drop Server'
, 'DT': 'Drop Table'
, 'DU': 'Drop User'
, 'DV': 'Drop View'
, 'DZ': 'Drop Zone'
, 'E ': 'Execute'
, 'EF': 'Execute Function'
, 'GC': 'Create Glop'
, 'GD': 'Drop Glop'
, 'GM': 'Glop Member'
, 'I ': 'Insert'
, 'IX': 'Index'
, 'MR': 'MonResource'
, 'MS': 'MonSession'
, 'NT': 'NonTemporal'
, 'OA': 'Override Dump'
, 'OD': 'Override Delete Policy'
, 'OI': 'Override Insert Policy'
, 'OP': 'Create Owner Procedure'
, 'OR': 'Override Restore'
, 'OS': 'Override Select Policy'
, 'OU': 'Override Update Policy'
, 'PC': 'Create Procedure'
, 'PD': 'Drop Procedure'
, 'PE': 'Execute Procedure'
, 'R ': 'Select'
, 'RF': 'Reference'
, 'RO': 'ReplControl'
, 'RS': 'Restore'
, 'SA': 'Security Constraint Assignment'
, 'SD': 'Security Constraint Definition'
, 'SH': 'Show'
, 'SR': 'SetResRate'
, 'SS': 'SetSesRate'
, 'ST': 'Statistics'
, 'TH': 'Ctcontrol'
, 'U ': 'Update'
, 'UM': 'UDT Method'
, 'UT': 'UDT Type'
, 'UU': 'UDT Usage'
, 'ZO': 'Zone Override'
}
