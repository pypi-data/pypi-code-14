#! /usr/bin/env python
"Generate DDL for Teradata Profiles using DBC information"

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

from collections import OrderedDict
from itertools import groupby
from .util import *

class Profile:
	def __init__(I, *opts):
		I.name, defacct, I.defdb, I.spool, I.temp, I.expire, I.pwmin, I.pwmax, I.pwdig, I.pwspec, I.pwwords, I.attempts, I.lockexp, I.reuse, I.qb, I.qbdef, I.comm = opts
		I.accts = []
		if defacct:
			I.accts.append(defacct)

	def ddl(I, gen_defaults=False):
		def toint(v): return int(v) if v != None else None

		opts = Opts([
			('Account',            quote(I.accts)),
			('Default Database',   I.defdb),
			('Spool',              toint(I.spool)),
			('Temporary',          toint(I.temp)),
			('Query_Band',         quote(I.qb))])

		pw_opts = Opts([
			('Expire',             I.expire),
			('MinChar',            I.pwmin),
			('MaxChar',            I.pwmax),
			('Digits',             quote(I.pwdig)),
			('SpecChar',           quote(I.pwspec)),
			('RestrictWords',      quote(I.pwwords)),
			('MaxLogonAttempts',   I.attempts),
			('LockedUserExpire',   I.lockexp),
			('Reuse',              I.reuse)])

		if pw_opts:
			opts.add('Password ({})'.format(pw_opts))

		cmd = 'Create Profile '+I.name;
		if opts:
			cmd += ' As ' + str(opts)

		return cmd+';'

	def comment(I):
		if I.comm:
			return "Comment On Profile {} As {};".format(I.name, quote(I.comm))


def add_args(p):
	p.add_argument("filter", metavar='PROFILE', default=['%'], nargs='*', help="Teradata profile name")


def genddl(args):
	sql = """\
SELECT ProfileName
     , DefaultAccount
     , DefaultDB
     , SpoolSpace
     , TempSpace
     , ExpirePassword
     , PasswordMinChar
     , PasswordMaxChar
     , PasswordDigits
     , PasswordSpecChar
     , PasswordRestrictWords
     , MaxLogonAttempts
     , LockedUserExpire
     , PasswordReuse
     , Queryband
     , QuerybandDefault
     , CommentString
  FROM {dbc.ProfileInfoV} P
 WHERE ProfileName {}""".format(mk_pred(args.filter),dbc=dbc)

	profs = OrderedDict([ (row[0], Profile(*row)) for row in execsql(sql,'ProfileInfo SQL') ])

	sql = """\
SELECT A.UserName
     , A.AccountName
  FROM {dbc.AccountInfoV} A
  JOIN {dbc.ProfileInfoV} P ON P.ProfileName = A.UserName AND P.DefaultAccount <> A.AccountName
 WHERE UserOrProfile = 'Profile'
   AND UserName {}""".format(mk_pred(args.filter),dbc=dbc)

	for p,rows in groupby(execsql(sql,'Accounts for Profile SQL'), key=lambda r:r[0]):
		profs[p].accts.extend([a for p,a in rows])

	for p in profs.values():
		yield p.ddl()
		if p.comm:
			yield p.comment()


def main():
	import sys
	sys.exit(enter(sys.modules[__name__]))
