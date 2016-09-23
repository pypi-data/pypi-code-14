# this is a function to print anything include list type 
def print_list(mylist,level=0):
	if isinstance(mylist,list):
		for each_item in mylist:
			print_list(each_item,level+1)
	else:
		for tabs in range(level-1):
			print ("\t"),
		print(mylist)
