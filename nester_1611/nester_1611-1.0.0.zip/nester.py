"""本函数用于循环显示列表中的元素"""
def print_lol(the_list):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else :
			print(each_item)


