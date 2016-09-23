# this is a function to print anything include list type 
def print_list(mylist):
	if isinstance(mylist,list):
		for each_item in mylist:
			print_list(each_item)
	else:
		print(mylist)
