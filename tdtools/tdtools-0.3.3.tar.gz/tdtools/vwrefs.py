#! /usr/bin/env python

"List Teradata view dependecies"

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

from tdtools import sqlcsr
from tdtools import util
from tdtools import tdtypes

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger()

class Err(Exception): pass

class Node(util.Node):
	def __init__(self, obj, parent):
		util.Node.__init__(self, parent)
		self.obj = obj


def main():
	try:
		args = user_args()

		with sqlcsr.cursor(args) as _csr:
			global csr, vwlist, recurse

			csr = util.EnhancedCursor(_csr)
			if csr.version < "14.10":
				raise Err('This script works on Teradata versions 14.10 or later')

			vwlist = parse2list(args.names, args.since, args.before)
			recurse = args.since == None and args.before == None

			if args.store:
				persist(args.store)
			else:
				display()

		return 0

	except Err as msg:
		logger.error(msg)
	except Exception as msg:
		logger.exception(msg)

	return 8


def user_args():
	global args

	import argparse
	import textwrap
	from datetime import datetime

	def ArgDate(d): return datetime.strptime(d, '%Y-%m-%d')

	p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description = __doc__, epilog=textwrap.dedent("""\
	Note: --store argument requires the table to have all columns shown in the example below.
	   CREATE TABLE ViewRefs
	   ( ViewDB    varchar(128) character set unicode not null
	   , ViewName  varchar(128) character set unicode not null
	   , RefDB     varchar(128) character set unicode not null
	   , RefName   varchar(128) character set unicode not null
	   ) PRIMARY INDEX(ViewDB,ViewName);"""))

	p.add_argument("names", metavar='VIEW', nargs='+', help="View name or pattern (eg dbc.qry%% dbc.tablesv)")
	p.add_argument(      '--since',    metavar='YYYY-MM-DD', type=ArgDate, help="only views created since the given date")
	p.add_argument(      '--before',   metavar='YYYY-MM-DD', type=ArgDate, help="only views created before the given date")
	p.add_argument('-u', '--store',    metavar='TBL',        help="Insert/Update references info in a table")
	p.add_argument('-v', '--verbose', default=0, action='count', help='print verbose log information. Use -vv for more details')

	sqlcsr.dbconn_args(p)

	args = p.parse_args()

	if   args.verbose > 1: logger.setLevel(logging.DEBUG)
	elif args.verbose > 0: logger.setLevel(logging.INFO)

	return args


def parse2list(names, since, before):
	from tdtools import vsch

	def mk_pred(dbtb):
		db, tb = dbtb.split('.') if '.' in dbtb else (dbtb, None)
		dbq = "DatabaseName {} '{}'".format('like' if '%' in db else '=', db)
		return dbq if tb == None else "({} and TableName {} '{}')".format(dbq, 'like' if '%' in tb else '=', tb)

	sql = """\
SELECT DatabaseName
     , TableName
  FROM {dbc.TablesV} T
 WHERE TableKind = 'V'
   AND ({})""".format( '\n    OR  '.join([mk_pred(dbtb) for dbtb in names]), dbc=vsch.dbc_schema())

	if since:
		sql += "\n   AND CreateTimestamp >= CAST('{}' AS TIMESTAMP(0))".format(since.isoformat())
	if before:
		sql += "\n   AND CreateTimestamp <  CAST('{}' AS TIMESTAMP(0))".format(before.isoformat())

	logger.info('About to execute view filter SQL:\n'+ sql)
	csr.execute(sql)

	return [ tdtypes.View(db,ob) for db,ob in csr.fetchall() ]


def display():

	def build_node(view, parent=None):
		node = Node(view, parent=parent)

		for ob in view.reflist:
			if recurse and isinstance(ob, tdtypes.View):
				node.children.append(build_node(ob, parent=view))
			else:
				node.children.append(Node(ob, parent=view))

		return node

	for vw in vwlist:
		for pfx, node in build_node(vw).tree_walk():
			print("{}{}".format(pfx,node.obj))


def persist(table):

	def ref_iterator():
		def view_iterator(vw):
			for ob in vw.reflist:
				yield vw.sch, vw.name, ob.sch, ob.name
				if recurse and isinstance(ob, tdtypes.View):
					yield from view_iterator(ob)

		for vw in vwlist:
			yield from view_iterator(vw)

	try:
		csr.executemany("DELETE FROM {} WHERE ViewDB = ? AND ViewName = ?".format(table), [(vw.sch, vw.name) for vw in vwlist] , batch=True)
		csr.executemany("INSERT INTO {}(ViewDB,ViewName,RefDB,RefName) VALUES(?,?,?,?)".format(table), ref_iterator() , batch=True)
	except sqlcsr.DatabaseError as msg:
		raise Err("Could not modify [{}]. Make sure the ID has SELECT, DELETE and INSERT permissions and right structure.".format(table)) from msg


if __name__ == '__main__':
	import sys
	sys.exit(main())
