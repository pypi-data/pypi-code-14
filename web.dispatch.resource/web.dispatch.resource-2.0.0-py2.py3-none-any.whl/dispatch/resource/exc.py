# encoding: utf-8

try:
	from webob.exc import HTTPMethodNotAllowed
except ImportError:  # pragma: no cover
	HTTPMethodNotAllowed = RuntimeError


class InvalidMethod(HTTPMethodNotAllowed):
	pass

