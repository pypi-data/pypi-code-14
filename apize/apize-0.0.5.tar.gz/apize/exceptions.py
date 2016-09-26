#!/usr/bin/env python3

from __future__ import absolute_import


class BadReturnVarType(Exception):
	def __init__(self, func):
		Exception.__init__(self,
			"'%s' function must be return a dict." % func
		)


class UnknowMethod(Exception):
	def __init__(self, method):
		Exception.__init__(self,
			"Unknow '%s' HTTP method." % method
		)
