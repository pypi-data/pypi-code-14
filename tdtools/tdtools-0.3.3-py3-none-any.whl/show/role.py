#! /usr/bin/env python
"Generate DDL for Teradata Roles using DBC information"

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

from .util import *

def add_args(p):
	p.add_argument("filter", metavar='ROLE', default=['%'], nargs='*', help="Teradata role name")


def genddl(args):
	sql = """\
SELECT RoleName
     , ExtRole
     , CommentString
  FROM {dbc.RoleInfoV} R
 WHERE RoleName {}""".format(mk_pred(args.filter),dbc=dbc)

	for role, isext, comm in execsql(sql,'RoleInfo SQL'):
		yield 'Create {}Role {};'.format('External ' if isext == 'Y' else '', role)
		if comm:
			yield "Comment On Role {} As {};".format(role,quote(comm))


def main():
	import sys
	sys.exit(enter(sys.modules[__name__]))
