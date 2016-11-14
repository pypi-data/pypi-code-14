"""
@author: Luo
@date: 2016/11/13
"""
def print_item(the_list,indent = False,level = 0,fn = sys.stdout):
	"""
	The function of looping output
	level: indentation of the list
	"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_item(each_item,indent,level + 1,fn)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end = '',file = fn)
			print(each_item,file = fn)