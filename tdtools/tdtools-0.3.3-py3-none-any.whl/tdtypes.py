"Python classes to represent Teradata objects"

from __future__ import (absolute_import, division, print_function, unicode_literals)

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

import logging
import xml.etree.ElementTree as ET
import re

from . import util
from . import sqlcsr

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger()

class Ident(str):
	def __str__(self):
		if re.match('^[a-z0-9][a-z0-9#$_]*$',str.__str__(self),re.I):
			return self
		return '"'+str.__str__(self).replace('"','""')+'"'


class DBObj:
	def __init__(self, sch, name, objtype=None):
		self.sch, self.name, self.objtype = Ident(sch), Ident(name), objtype

	def __str__(self):
		return '{}.{}'.format(self.sch,self.name)

	def __repr__(self):
		return "{}('{}','{}')".format(self.__class__.__name__,self.sch,self.name)

	@staticmethod
	def findall(*wildcards, objtypes=''):
		from . import vsch

		def mk_pred(dbtb):
			db, tb = dbtb.split('.') if '.' in dbtb else (dbtb, None)
			dbq = "DatabaseName {} '{}'".format('like' if '%' in db else '=', db)
			return dbq if tb == None else "({} and TableName {} '{}')".format(dbq, 'like' if '%' in tb else '=', tb)

		sql = """\
SELECT DatabaseName
     , TableName
     , TableKind
  FROM {dbc.TablesV} T
 WHERE ({})""".format( '\n    OR  '.join([mk_pred(dbtb) for dbtb in wildcards]), dbc=vsch.dbc_schema())

		if objtypes:
			sql += '\n  AND TableKind IN ({})'.format(', '.join(["'{}'".format(t) for t in objtypes]))

		sqlcsr.csr.execute(sql)

		oblist = []
		for db, tb, tp in sqlcsr.csr.fetchall():
			if tp == 'T' or tp == 'O':
				oblist.append(Table(db,tb,objtype=tp))
			elif tp == 'V':
				oblist.append(View(db,tb))
			else:
				oblist.append(DBObj(db,tb,tp))

		return oblist


class Table(DBObj):
	"""Represents Teradata table object. All attributes except schema+name are
	evaluated lazily."""

	def __init__(self, sch, name, chk_exists=False, objtype='T'):
		DBObj.__init__(self, sch, name, objtype)
		self._collist = None

		if chk_exists:
			self._getdef()  # will throw an exception if table doesn't exist

	def _getdef(self):
		if self._collist == None:
			csr = util.EnhancedCursor(sqlcsr.csr)
			csr.execute('SHOW IN XML TABLE ' + str(self))
			root = ET.fromstring(csr.fetchxml())
			xml = root.find('./Table')

			self._ismultiset  = xml.attrib['kind'] == 'Multiset'
			self._hasfallback = xml.attrib['fallback'] == 'true'

			self._collist = [Column.fromxml(c) for c in root.find('./Table/ColumnList')]
			self._ixlist  = [Index.fromxml(i,self) for i in root.find('./Table/Indexes')]

		return self

	@property
	def collist(self): return self._getdef()._collist

	@property
	def ixlist(self): return self._getdef()._ixlist

	def _col_lookup(self, name):
		for c in self._collist:
			if c.name == name:
				return c
		logger.error('Table [{}] has no column named [{}]'.format(self, name))

	def _collist_fromxml(self, xml):
		return [self._col_lookup(c.attrib['name']) for c in xml.find('./ColumnList')]

	@property
	def picols(self):
		for ix in self.ixlist:
			if ix.prim:
				return ix.cols
		return []

	@property
	def pkcols(self):
		for ix in self.ixlist:
			if ix.pkey:
				return ix.cols
		return []


class View(DBObj):
	def __init__(self, sch, name, chk_exists=False):
		DBObj.__init__(self, sch, name, 'V')
		self._collist = self._reflist = None


	def _getdef(self):
		if self._collist == None:
			csr = util.EnhancedCursor(sqlcsr.csr)
			csr.execute('SHOW IN XML VIEW ' + str(self))
			root = ET.fromstring(csr.fetchxml()).find('./View')

			self._collist = [Column.fromxml(c) for c in root.findall('./ColumnList/Column')]

			self._reflist = []
			if not root.find('./RefList'):
				logger.warn('XML definition for [{}] did not return any references'.format(str(self)))
			else:
				for r in root.find('./RefList'):
					sch, name, tv = r.attrib['dbName'], r.attrib['name'], r.attrib['type']
					if tv == 'View':
						self._reflist.append(View(sch,name))
					else:
						self._reflist.append(Table(sch,name))

		return self

	@property
	def collist(self): return self._getdef()._collist

	@property
	def reflist(self): return self._getdef()._reflist


class SQLRegister(str): pass

class Column:
	def __init__(self, name, coltype=None, nullable=True, defval=None, fmtstr=None):
		self.name, self.coltype, self.nullable, self.defval, self.fmtstr = Ident(name), coltype, nullable, defval, fmtstr

	def sqltype(self):
		return self.coltype

	def __repr__(self):
		return "Column('{}','{}')".format(self.name, self.sqltype())

	def __str__(self):
		return self.name

	def __eq__(self, other):
		if other == None:
			return False
		if isinstance(other,str):
			return (self.name == other)
		if isinstance(other, Column):
			return self.__dict__ == other.__dict__

		return False

	@staticmethod
	def fromxml(cdef):
		name = cdef.attrib['name']

		attr = { 'nullable': cdef.attrib['nullable'] == 'true' }

		defval = cdef.find('Default')
		if defval:
			attr['defval'] = SQLRegister(defval.attrib['type']) if 'type' in defval.attrib else defval.attrib['value']
		if 'format' in cdef.attrib:
			attr['fmtstr'] = cdef.attrib['format']

		t = cdef.find('DataType')[0]

		if   t.tag == 'Char':     return CharColumn(name, int(t.attrib['length']), varchar=t.attrib['varying']=='true', charset=t.attrib['charset'], **attr)

		elif t.tag == 'Integer':  return IntColumn(name, 4, **attr)
		elif t.tag == 'SmallInt': return IntColumn(name, 2, **attr)
		elif t.tag == 'ByteInt':  return IntColumn(name, 1, **attr)
		elif t.tag == 'BigInt':   return IntColumn(name, 8, **attr)
		elif t.tag == 'Decimal':  return DecColumn(name, int(t.attrib['precision']), int(t.attrib['scale']), **attr)
		elif t.tag == 'Float':    return FloatColumn(name, **attr)

		elif t.tag == 'Date':     return DateColumn(name, **attr)
		elif t.tag == 'Time':     return TimeColumn(name, int(t.attrib['fractionalSecondsPrecision']), **attr)
		elif t.tag == 'TimeStamp':return TimestampColumn(name, int(t.attrib['fractionalSecondsPrecision']), **attr)
		elif t.tag.startswith('Interval'): return IntervalColumn(name, t.tag[8:], int(t.attrib['precision']), **attr)

		elif t.tag == 'JSON':     return JsonColumn(name, int(t.attrib['size']), **attr)
		elif t.tag == 'UDT' and t.attrib['name'] == "SYSUDTLIB.XML": return XmlColumn(name, **attr)

		return Column(name, coltype=t.tag.upper(), **attr)


class CharColumn(Column):
	def __init__(self, name, size, varchar=False, cs=False, charset=None, **attr):
		Column.__init__(self, name, **attr)
		self.size, self.varchar, self.cs, self.charset = size, varchar, cs, charset

	def sqltype(self):
		return '{}CHAR({})'.format('VAR' if self.varchar else '', self.size)


class TimeColumn(Column):
	def __init__(self, name, frac, **attr):
		Column.__init__(self, name, **attr)
		self.frac = frac

	def sqltype(self):
		return '{}({})'.format(self.coltype, self.frac)


class TimestampColumn(TimeColumn):
	def __init__(self, name, frac, **attr):
		Column.__init__(self, name, **attr)
		self.frac = frac

	def sqltype(self):
		return 'TIMESTAMP({})'.format(self.frac)


class IntColumn(Column):
	def __init__(self, name, size, **attr):
		Column.__init__(self, name, **attr)
		self.size = size

	def sqltype(self):
		return {4:'INTEGER',2:'SMALLINT',1:'BYTEINT',8:'BIGINT'}[self.size]


class DecColumn(Column):
	def __init__(self, name, precision, scale, **attr):
		Column.__init__(self, name, **attr)
		self.precision, self.scale = precision, scale

	def sqltype(self):
		return 'DECIMAL({},{})'.format(self.precision, self.scale)


class IntervalColumn(Column):
	def __init__(self, name, types, precision, **attr):
		Column.__init__(self, name, **attr)
		self.precision = precision
		self.type1, self.type2 = types.split('To')

	def sqltype(self):
		prec = '' if self.precision == 2 else '({})'.format(self.precision)
		return 'INTERVAL {}{} TO {}'.format(self.type1.upper(), prec, self.type2.upper())


class JsonColumn(Column):
	def __init__(self, name, size, **attr):
		Column.__init__(self, name, coltype='JSON', **attr)
		self.size = size
class DateColumn(Column):
	def __init__(self, name, **attr):
		Column.__init__(self, name, coltype='DATE', **attr)
class FloatColumn(Column):
	def __init__(self, name, **attr):
		Column.__init__(self, name, coltype='REAL', **attr)
class XmlColumn(Column):
	def __init__(self, name, **attr):
		Column.__init__(self, name, coltype='XML', **attr)


class Index(object):
	def __init__(self, name, cols, prim=False, uniq=False, pkey=False, allness=False, o_col=None, o_byval=False, ptlist=None):
		self.name, self.cols, self.prim, self.uniq, self.pkey, self.allness, self.o_col, self.o_byval, self.ptlist = name, cols, prim, uniq, pkey, allness, o_col, o_byval, ptlist

	def __repr__(self):
		return 'Index {}(cols=({}), prim={}, uniq={}, pkey={}, all={}, order={}, type={}, ptlist={})'.format(self.name or '', ','.join([c.name for c in self.cols]), self.prim, self.uniq, self.pkey, self.allness, self.o_col or '', self.o_byval or '', self.ptlist)

	@staticmethod
	def fromxml(xml, tbl):
		name = xml.get('name')

		ptlist = []
		ptlist_x = xml.find('PartitioningList')
		if ptlist_x:
			ptlist = [ Partition.fromxml(pt, tbl) for pt in ptlist_x ]

		if xml.tag == 'NoPrimaryIndex':
			return Index(name,[],ptlist=ptlist)

		o_col = o_byval = None
		if 'OrderBy' in xml:
			o_col = tbl._col_lookup(xml['OrderBy'].attrib['name'])
			o_byval = xml['OrderBy'].attrib['type'] == 'value'

		return Index(name
				, tbl._collist_fromxml(xml)
				, prim = xml.tag=='PrimaryIndex'
				, uniq = xml.attrib['unique']=='true'
				, pkey = xml.get('implicitIndexFor','None') == "PrimaryKeyConstraint"
				, allness = xml.get('allOption',"false") == 'true'
				, o_col = o_col
				, o_byval = o_byval
				, ptlist = ptlist
				)


class Partition:
	def __init__(self, level, extra=0):
		self.level, self.extra = level, extra

	@staticmethod
	def fromxml(xml, tbl):
		level, extra = xml.attrib['level'], xml.get('extraPartitions',0)

		if xml.tag == 'RowPartitioning':
			return RowPartition(level, xml.attrib['expression'], extra=extra)

		if xml.tag == 'ColumnPartitioning':
			return ColPartition(level, [ColGroup.fromxml(cg,tbl) for cg in xml], extra=extra)


class RowPartition(Partition):
	def __init__(self, level, expr, extra=0):
		Partition.__init__(self, level, extra)
		self.expr = expr

	def __repr__(self):
		return 'RowPartition("{}", levl={}, extra={})'.format(self.expr, self.level, self.extra)


class ColPartition(Partition):
	def __init__(self, level, colgrps, extra=0):
		Partition.__init__(self, level, extra)
		self.colgrps = colgrps

	def __repr__(self):
		return 'ColPartition({}, levl={}, extra={})'.format(self.colgrps, self.level, self.extra)


class ColGroup(list):
	def __init__(self, copy=None, compressed=False):
		if copy:
			self.extend(copy)
		self.compressed = compressed

	def __repr__(self):
		return 'ColGroup({}, Compressed={})'.format([c.name for c in self], self.compressed)

	@staticmethod
	def fromxml(xml,tbl):
		cg = ColGroup(compressed = xml.get('autoCompress',"false") == "true")
		cg.extend(tbl._collist_fromxml(xml))

		return cg
