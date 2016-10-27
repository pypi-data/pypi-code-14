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
			sleep(3)
		finally:
			copy(oclp)
		exit(0)

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
        '-p', '--passcrypt',
        dest='pcr', metavar='CRYPTFILE',
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
	args = pars.parse_args()
	pargs = [a for a in ['dbg' if args.dbg else None] if a]
	pkwargs = {'aal': True if args.aal else None}
	if args.usr:
		pkwargs['user'] = args.usr
	oclp = paste()
	if args.yks is not False:
		if 'YKSERIAL' in environ.keys():
			ykser = environ['YKSERIAL']
		ykser = args.yks if args.yks else None
		forkwaitclip(ykchalres(inputgui(), ykser=ykser), oclp)
		exit(0)
	pcm = PassCrypt(*pargs, **pkwargs)
	if args.lst is not False:
		__pc = pcm.lspw(args.lst)
		if not __pc:
			fatal('could not decrypt')
		elif not [e for e in __pc if e]:
			fatal('no entry matching', args.lst)
		elif args.lst is None:
			print(tabd(__pc))
			exit(0)
		elif len(__pc) == 2:
			xnotify('%s: %s'%(args.lst, __pc[1]))
		forkwaitclip(__pc[0], oclp)
	elif args.add:
		if not pcm.adpw(args.add):
			fatal('could not add entry', args.add)
		__pc = pcm.lspw(args.add)
	elif args.chg:
		if not pcm.chpw(args.chg):
			fatal('could not change entry', args.chg)
		__pc = pcm.lspw(args.chg)
		print(args.chg, '=', pcm.lspw(args.chg))
	elif args.rms:
		for r in args.rms:
			if not pcm.rmpw(r):
				fatal('could not delete entry', r)
		print(tabd(pcm.lspw()))
	else:
		__in = inputgui()
		__pc = pcm.lspw(__in)
		if __pc and len(__pc) == 2:
			xnotify('%s: %s'%(__in, __pc[1]))
		forkwaitclip(__pc[0], oclp)
		exit(0)
	__pc = {args.lst: ['*'*len(__pc[0]), __pc[1]]}
	print(tabd(__pc))
