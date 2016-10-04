#This is the "test3.py" module and it provides one function called print_list()
#which print the lists that may or may not include nested lists.
def print_list(list_name):
	for each_item in list_name:
		if isinstance(each_item,list):
			print_list(each_item)
		else:
			print(each_item)
