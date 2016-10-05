#! /usr/bin/env python
# -*- coding: utf8 -*-

"List Teradata Database hierarcy"

import logging

from tdtools import sqlcsr
from tdtools import util
from tdtools import vsch

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

logging.basicConfig(format="%(levelname)s: %(message)s")
logger = logging.getLogger()

class Dbase(util.Node):
	def __init__(self, parent, name, alloc=0, used=0):
		util.Node.__init__(self, parent)
		self.name, self.alloc, self.used = name, int(alloc), int(used)

	def alloc_rollup(self):
		return self.alloc + sum([c.alloc_rollup() for c in self.children])

	def used_rollup(self):
		return self.used + sum([c.used_rollup() for c in self.children])


def main():
	try:
		global args

		args = user_args()

		sql = build_sql(args)

		if args.sql:
			print(sql)
			return

		with sqlcsr.cursor(args) as csr:
			csr.execute(sql)
			tree = build_tree(csr.fetchall() if args.sizes else [(d,l,0,0) for d,l in csr.fetchall()])

		print_tree(tree, fancy=args.fancy, detailed=args.sizes, rollup=args.cumulative)

		return 0

	except Exception as msg:
		logger.exception(msg)
		return 8


def user_args():
	from argparse import ArgumentParser

	p = ArgumentParser(description = __doc__)

	p.add_argument("seed", metavar='DB', nargs='?', default='dbc', help="Database name (default DBC)")
	p.add_argument("-a", "--ancestors", action='store_true', help="show ancestors instead of descendents")
	p.add_argument("--sql",             action='store_true', help="show generated SQL; do not run it")
	p.add_argument("--max-depth", metavar='INT', type=int,   help="limit hierarchy depth to the specified value")
	p.add_argument("-Z", "--non-zero",  action='store_true', help="only show databases with non-zero PERM space")
	p.add_argument("-z", "--sizes",     action='store_true', help="show database MaxPerm and CurrPerm sizes")
	p.add_argument("-c", "--cumulative",action='store_true', help="include child database sizes with parent database sizes")
	p.add_argument('-F', '--no-fancy',  dest='fancy', default=True, action='store_false', help='Do not use unicode box characters for drawing')

	g = p.add_mutually_exclusive_group()
	g.add_argument('-d', '--only-db',   dest='dbkind', action='store_const', const='D', help='list only databases')
	g.add_argument('-u', '--only-users',dest='dbkind', action='store_const', const='U', help='list only users')

	p.add_argument('-v', '--verbose',  default=0, action='count', help='print verbose log information. Use -vv for more details')

	sqlcsr.dbconn_args(p)

	args = p.parse_args()

	if   args.verbose > 1: logger.setLevel(logging.DEBUG)
	elif args.verbose > 0: logger.setLevel(logging.INFO)

	return args


def build_sql(args):
	dbc = vsch.dbc_schema()

	# reverse parent and child if ancestors are requested
	P = 'C' if args.ancestors else 'P'
	C = 'C' if P == 'P' else 'P'

	where = ['c.CDB is not null', 'p.DB = c.PDB']

	if args.max_depth:
		where.append("Depth < {}".format(args.max_depth))
	if args.dbkind:
		where.append("DBKind = '{}'".format(args.dbkind))
	if args.non_zero:
		where.append("PermSpace > 0")

	sql =  """\
with recursive hierarchy(DB, DBPath, Depth, AllocSize) as
(
    select DB
         , cast(DB as varchar(30000))
         , 0
         , PermSpace
      from ancestry s
     where DB = '{}'

     union all

    select c.CDB
         , DBPath || ':' || CDB
         , Depth + 1
         , c.PermSpace
      from ancestry c
         , hierarchy p
     where {}
)

, ancestry as
(
    select DatabaseName          as DB
         , DatabaseName          as {}DB
         , case when DatabaseName = 'DBC'
                then NULL
                else OwnerName
           end                   as {}DB
         , PermSpace
         , DBKind
      from {dbc.DatabasesV}
)
""".format(args.seed, "\n       and ".join(where), C, P, dbc=dbc)

	if args.sizes:

		sql += """
select DB
     , Depth
     , AllocSize
     , UsedSize

  from hierarchy h

  join (
        select DatabaseName
             , sum(CurrentPerm) As UsedSize
          from {dbc.DiskSpaceV}
         group by 1
       ) z
    on z.DatabaseName = h.DB

 order by DBPath""".format(dbc=dbc)

	else:

		sql += """
select h.DB
     , h.Depth
  from hierarchy h
 order by DBPath"""

	logger.info('SQL: '+sql)

	return sql


def build_tree(dbinfo):
	prev_level = 0
	root = parent = None

	for name, level, alloc, used in dbinfo:

		if level > prev_level:
			parent = parent.children[-1] if parent else root
		elif level < prev_level:
			parent = parent.parent

		node = Dbase(parent,name,alloc,used)

		if parent:
			parent.children.append(node)
		else:
			root = node

		prev_level = level

	return root


def print_tree(tree, fancy=False, detailed=False, rollup=False):
	if detailed:
		if rollup:
			formatter = lambda node,pfx: "{:<30} {:18,} {:18,}".format(pfx+node.name, node.alloc_rollup(), node.used_rollup())
		else:
			formatter = lambda node,pfx: "{:<30} {:18,} {:18,}".format(pfx+node.name, node.alloc, node.used)
	else:
		formatter = lambda node,pfx: pfx+node.name

	util.Links.set_style(util.Links.fancy if fancy else util.Links.simple)

	for pfx, node in tree.tree_walk():
		print(formatter(node,str(pfx)))


if __name__ == '__main__':
	import sys
	sys.exit(main())
