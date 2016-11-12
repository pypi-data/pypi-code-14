def print_list(list_name):
	for each_item in list_name:
		if isinstance(each_item,list):
			print_list(each_item)
		else:
			print(each_item)
