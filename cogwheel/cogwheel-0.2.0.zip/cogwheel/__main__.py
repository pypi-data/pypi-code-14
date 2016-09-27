import sys
from .compiler import Compile

projects = sys.argv[1:]

if not projects:
	projects = ['.']

for projet in projects:
	Compile(projet)
