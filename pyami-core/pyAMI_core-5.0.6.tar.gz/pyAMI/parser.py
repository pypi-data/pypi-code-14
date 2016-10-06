# -*- coding: utf-8 -*-
from __future__ import (division, print_function, unicode_literals)
#############################################################################
# Author  : Jerome ODIER, Jerome FULACHIER, Fabian LAMBERT, Solveig ALBRAND
#
# Email   : jerome.odier@lpsc.in2p3.fr
#           jerome.fulachier@lpsc.in2p3.fr
#           fabian.lambert@lpsc.in2p3.fr
#           solveig.albrand@lpsc.in2p3.fr
#
# Version : 5.X.X (2014)
#
#############################################################################

import re, pyAMI.exception

#############################################################################

PATTERN1 = re.compile(
	'^\\s*([a-zA-Z][a-zA-Z0-9]*)'
)

PATTERN2 = re.compile(
	'^[-]*([a-zA-Z][a-zA-Z0-9]*)\\s*=\\s*\"((?:\\\\\"|[^\"])*)\"'
)

PATTERN3 = re.compile(
	'^[-]*([a-zA-Z][a-zA-Z0-9]*)\\s*=\\s*([^\\s]+)'
)

PATTERN4 = re.compile(
	'^[-]*([a-zA-Z][a-zA-Z0-9]*)'
)

#############################################################################

def parse(args):

	if not isinstance(args, basestring):
		s = ''

		for arg in args:
			s += _shell_barrier(arg) + ' '

	else:
		s = args.__str__()

	i = 0x0000
	l = len(s)

	#####################################################################
	# PARSE COMMAND                                                     #
	#####################################################################

	m = PATTERN1.search(s)

	if not m is None:
		result = m.group(1)
		i += len(result)
	else:
		raise pyAMI.exception.Error('command syntax error, missing command name')

	#####################################################################
	# PARSE ARGUMENTS                                                   #
	#####################################################################

	args = {}

	while i < l:
		#############################################################
		# EAT SPACE                                                 #
		#############################################################

		if s[i].isspace():
			i += 1
			continue

		#############################################################
		# EAT ARGUMENT                                              #
		#############################################################

		m = PATTERN2.search(s[i: ])
		if m is None:

			m = PATTERN3.search(s[i: ])
			if m is None:

				m = PATTERN4.search(s[i: ])
				if m is None:

					raise pyAMI.exception.Error('command syntax error, invalid argument syntax')

		#############################################################

		if len(m.groups()) < 2:
			result += ' -%s' % (m.group(1))
		else:
			result += ' -%s="%s"' % (m.group(1), m.group(2))

		i += len(m.group(0))

	#####################################################################

	return result

#############################################################################

shell_barrier = False

#############################################################################

def _shell_barrier(arg):

	if shell_barrier:

		idx = arg.find('=')

		if idx != -1:
			left_part = arg[: idx + 0].strip()
			right_part = arg[idx + 1: ].strip()

			if len(right_part) >= 2:

				if (right_part[0] != '\'' or right_part[-1] != '\'')\
				   and                                              \
				   (right_part[0] != '\"' or right_part[-1] != '\"'):

					arg = '%s="%s"' % (left_part, right_part)

	return arg

#############################################################################
