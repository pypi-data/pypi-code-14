#! /usr/bin/env python
"Wrapper around Teradata's SHOW command"

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

import sys
import os
import os.path as p

from itertools import groupby
from .util import *
from .. import sqlcsr

obj_t = {'T':'Table', 'O':'Table', 'V':'View', 'C':'Temporary Table', 'I':'Join Index', 'G':'Trigger', 'M':'Macro', 'P':'Procedure'}

class DBObj:
	def __init__(self, sch, name, kind):
		self.sch, self.name, self.kind = sch, name, kind

	def __str__(self):
		return '"{}"."{}"'.format(self.sch, self.name)


def add_args(p):
	from datetime import datetime

	def ArgDate(d): return datetime.strptime(d, '%Y-%m-%d')

	p.add_argument("filter",           metavar='DBObj', nargs='+',   help="database object name")
	p.add_argument("-t", '--type',     metavar='KIND',  choices = obj_t, dest="types", action='append', help="Limit objects to selected types ({})".format(','.join(sorted(obj_t))))
	p.add_argument(      '--no-stats', dest='stats',    default=True, action='store_false', help="Do not generate stats defintions")
	p.add_argument(      '--since',    metavar='YYYY-MM-DD', type=ArgDate, help="only consider objects ALTERed since the given date")
	p.add_argument(      '--before',   metavar='YYYY-MM-DD', type=ArgDate, help="only consider objects ALTERed before the given date")
	p.add_argument('-w', '--write',    action='store_true',          help='Create a file for each database object')


def genddl(args):

	for typ, grp1 in groupby(getobjs(args.filter,args.types,args.since,args.before), key=lambda o:o.kind):

		for db, grp2 in groupby(grp1, key=lambda o:o.sch):
			yield '\nDatabase {0};\n'.format(db)

			for o in grp2:
				try:
					yield obj_ddl(o, args.write, args.stats)
				except sqlcsr.DatabaseError as msg:
					logger.warn("Skipped {}, error:{}'".format(o,msg))


def getobjs(objects, types, since=None, before=None):
	def mk_pred(dbtb):
		db, tb = dbtb.split('.') if '.' in dbtb else (dbtb, None)
		dbq = "DatabaseName {} '{}'".format('like' if '%' in db else '=', db)
		if tb == None:
			return dbq
		return "({} and TableName {} '{}')".format(dbq, 'like' if '%' in tb else '=', tb)

	sql = """\
SELECT DatabaseName
     , TableName
     , TableKind
  FROM {dbc.TablesV} T
 WHERE ({})""".format( '\n    OR  '.join([mk_pred(dbtb) for dbtb in objects]), dbc=dbc )

	if types:
		sql += "\n   AND TableKind IN {0}".format(sql_in_list(types))
	if since:
		sql += "\n   AND LastAlterTimestamp >= CAST('{}' AS TIMESTAMP(0))".format(since.isoformat())
	if before:
		sql += "\n   AND LastAlterTimestamp <  CAST('{}' AS TIMESTAMP(0))".format(before.isoformat())

	sql += """
 ORDER BY CASE TableKind
               WHEN 'T' THEN 0
               WHEN 'O' THEN 0
               WHEN 'C' THEN 0
               WHEN 'G' THEN 1
               WHEN 'I' THEN 2
               WHEN 'V' THEN 3
                        ELSE 4
          END
        , CreateTimestamp"""

	return [DBObj(db,ob,k) for db,ob,k in execsql(sql, 'Object list SQL')]


def obj_ddl(obj, write, stats):
	def show(sql):
		ddl = ''.join([l[0].replace('\r','\n') for l in execsql('SHOW ' + sql)]).rstrip()
		if ddl[-1] != ';':
			ddl += ';'

		return ddl

	ddl = show('{} "{}"."{}"'.format(obj_t[obj.kind], obj.sch, obj.name))

	if stats and obj.kind in ['T','O','N','I']:
		try:
			ddl += '\n\n' + show('STATS ON "{}"."{}"'.format(obj.sch, obj.name))
		except sqlcsr.DatabaseError as msg:
			logger.info('SHOW STATS ON {} failed.'.format(str(obj)))

	if write:
		mk_dbfolder(obj.sch)
		fname = p.join( obj.sch, obj.name + '.' + {'P':'sp'}.get(obj.kind,'sql') )
		logger.debug('Writing DDL of "{}" to "{}"'.format(obj,fname))
		with open(fname, 'w') as out:
			print(ddl, file=out)
		return '.{} file={}'.format('compile' if obj.kind == 'P' else 'run', fname)

	else:
		return ddl + '\n'


folders = set()
def mk_dbfolder(db):
	if db in folders:
		return

	if not p.exists(db):
		os.mkdir(db)
	elif not p.isdir(db):
		raise Err('[{}] exists and is not a directory'.foramt(db))

	folders.add(db)


def main():
	import sys
	sys.exit(enter(sys.modules[__name__]))
