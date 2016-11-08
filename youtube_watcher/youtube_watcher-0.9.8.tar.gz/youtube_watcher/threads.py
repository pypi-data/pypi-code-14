#!/usr/bin/env python3


import threading


class asthread(object):
	def __init__(self, daemon=False):
		self.daemon = daemon

	def __call__(self, function):
		def inner(*args, **kwargs):
			thread = threading.Thread(target=function, args=args,
									  kwargs=kwargs)
			thread.daemon = self.daemon
			thread.start()
			return None
		return inner
