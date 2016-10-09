#!/usr/bin/env python3

class BadReturnVarType(Exception):
	def __init__(self, func):
		Exception.__init__(self,
			"function '%s' must be return a dict." % func
		)

