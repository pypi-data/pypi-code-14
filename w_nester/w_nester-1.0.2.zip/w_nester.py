import sys
def list_out(_list, indent=False, level=0, fh=sys.stdout):
	for x in _list:
		if isinstance(x, list):
			list_out(x, indent, level+1, fh)
		else:
			if indent:
				for y in range(level):
					print("\t", end='', file=fh)
					print(y, file=fh)
			print(x, file=fh)
