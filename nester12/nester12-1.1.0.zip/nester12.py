from __future__ import print_function
def print_lol(klist,level):
	for each_item in klist:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for tabs in range(0,level):
				print("\t",end="")
			print(each_item)

