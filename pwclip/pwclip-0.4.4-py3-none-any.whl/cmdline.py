#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is free software by d0n <d0n@janeiskla.de>
#
# You can redistribute it and/or modify it under the terms of the GNU -
# Lesser General Public License as published by the Free Software Foundation
#
# This is distributed in the hope that it will be useful somehow.
# !WITHOUT ANY WARRANTY!
#
# Without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
"""pwclip main program"""

# global & stdlib imports
import sys

from os import environ, path, fork

from os.path import isfile

from yaml import load

from argparse import ArgumentParser

from time import sleep

# local relative imports
from colortext import tabd, fatal

from system import inputgui, copy, paste, xnotify

from cypher import PassCrypt, ykchalres

from pwclip.__pkginfo__ import version

def forkwaitclip(text, oclp, wait=3):
	if text != oclp and fork() == 0:
		try:
			copy(text)
			sleep(int(wait))
		finally:
			copy(oclp)
	exit(0)

def __passreplace(pwlist):
	__pwcom = ['*'*len(pwlist[0])]
	if len(pwlist) > 1:
		__pwcom.append(pwlist[1])
	return __pwcom

def __dictreplace(pwdict):
	__pwdict = {}
	for (usr, ent) in pwdict.items():
		if isinstance(ent, dict):
			__pwdict[usr] = {}
			for (u, e) in ent.items():
				__pwdict[usr][u] = __passreplace(e)
		elif ent:
			__pwdict[usr] = __passreplace(ent)
	return __pwdict


# global default variables
def cli():
	_me = path.basename(__file__)
	cfg = path.expanduser('~/.config/%s.yaml'%_me)
	try:
		with open(cfg, 'r') as cfh:
			cfgs = load(cfh.rad())
	except FileNotFoundError:
		cfgs = {}
	pars = ArgumentParser() #add_help=False)
	pars.set_defaults(**cfgs)
	pars.add_argument(
        '--version',
        action='version', version='%(prog)s-v'+version)
	pars.add_argument(
        '-D', '--debug',
        dest='dbg', action='store_true', help='debugging mode')
	pars.add_argument(
        '-A', '--all',
        dest='aal', action='store_true',
        help='switch to all users entrys (instead of current user only)')
	pars.add_argument(
        '-s', '--show-passwords',
        dest='sho', action='store_true',
        help='switch to display passwords (replaced with * by default)')
	pars.add_argument(
        '-a', '--add',
        dest='add', metavar='ENTRY',
        help='add ENTRY (password will be asked interactivly)')
	pars.add_argument(
        '-c', '--change',
        dest='chg', metavar='ENTRY',
        help='change ENTRY (password will be asked interactivly)')
	pars.add_argument(
        '-d', '--delete',
        dest='rms', metavar='ENTRY', nargs='+',
        help='delete ENTRY(s) from the passcrypt list')
	pars.add_argument(
        '-l', '--list',
        nargs='?', default=False,
        dest='lst', metavar='PATTERN',
        help='search entry matching PATTERN if given otherwise list all')
	pars.add_argument(
        '--yaml',
		dest='yml', metavar='YAMLFILE',
		default=path.expanduser('~/.pwd.yaml'),
        help='set location of one-time YAMLFILE to read')
	pars.add_argument(
        '-p', '--passcrypt',
        dest='pcr', metavar='CRYPTFILE',
        default=path.expanduser('~/.passcrypt'),
        help='set location of CRYPTFILE to use for gpg features')
	pars.add_argument(
        '-r', '--recipients',
        dest='rcp', metavar='RECIPIENT',
        help='gpg recipients (identifier) for GPG-Keys to use')
	pars.add_argument(
        '-u', '--user',
        dest='usr', metavar='USER',
        help='query entrys of USER (defaults to current user)')
	pars.add_argument(
        '-y', '--ykserial',
        nargs='?', default=False,
        dest='yks', metavar='SERIAL',
        help='switch to yubikey mode and optionally set SERIAL of yubikey')
	pars.add_argument(
        'time',
        nargs='?', default=3, metavar='seconds', type=int,
        help='time to wait before resetting clip (default is 3 max 3600)')
	args = pars.parse_args()
	pargs = [a for a in [
        'dbg' if args.dbg else None,
        'aal' if args.aal else None,
        'sho' if args.sho else None] if a]
	pkwargs = {}
	if args.pcr:
		pkwargs['crypt'] = args.pcr
	if args.usr:
		pkwargs['user'] = args.usr
	if args.yml:
		pkwargs['plain'] = args.yml
	if not isfile(pkwargs['plain']) and \
          not isfile(pkwargs['crypt']) and args.yks is False:
		fatal(
            'if not in yubi mode either yaml input file', pkwargs['plain'],
            'or already written passcrypt', pkwargs['crypt'], 'must exsist')
	oclp = paste()
	if args.yks is not False:
		args.time = args.yks if args.yks and len(args.yks) < 6 else args.time
		if 'YKSERIAL' in environ.keys():
			ykser = environ['YKSERIAL']
		ykser = args.yks if args.yks and len(args.yks) >= 6 else None
		forkwaitclip(ykchalres(inputgui(), ykser=ykser), oclp, args.time)
		exit(0)
	if args.lst and args.lst.isdigit() and int(args.lst) <= 3600:
		args.time = int(args.lst)
		args.lst = None
	for a in (args.lst, args.add, args.chg):
		if a and len(a) < 2:
			fatal('input', a, 'is too short')
	pcm = PassCrypt(*pargs, **pkwargs)
	if args.lst is not False:
		__ent = pcm.lspw(args.lst)
		if not __ent:
			fatal('could not decrypt')
		elif __ent and args.lst and not __ent[args.lst]:
			fatal('could not find entry for', args.lst, 'in', pkwargs['crypt'])
		elif args.lst and __ent:
			__pc = __ent[args.lst]
			if __pc:
				if len(__pc) == 2:
					xnotify('%s: %s'%(args.lst, __pc[1]), wait=args.time)
				forkwaitclip(__pc[0], oclp, args.time)
	elif args.add:
		if not pcm.adpw(args.add):
			fatal('could not add entry', args.add)
		__ent = pcm.lspw(args.add)
	elif args.chg:
		if not pcm.chpw(args.chg):
			fatal('could not change entry', args.chg)
		__ent = pcm.lspw(args.chg)
	elif args.rms:
		for r in args.rms:
			if not pcm.rmpw(r):
				fatal('could not delete entry', r)
		__ent = pcm.lspw()
	else:
		__in = inputgui()
		if not __in:
			exit(1)
		__ent = pcm.lspw(__in)
		if __ent:
			if not __ent[__in]:
				fatal(
                    'could not find entry for',
                    __in, 'in', pkwargs['crypt'])
			__pc = __ent[__in]
			if __pc:
				if len(__pc) == 2:
					xnotify('%s: %s'%(__in, __pc[1]), args.time)
				forkwaitclip(__pc[0], oclp, args.time)
	if not args.sho:
		__ent = __dictreplace(__ent)
	print(tabd(__ent))
