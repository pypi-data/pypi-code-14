# in python2, mock has to be installed as a pip package.
# in python3, it's included with the unittest module.
try:
	from unittest import mock
except ImportError:
	import mock
