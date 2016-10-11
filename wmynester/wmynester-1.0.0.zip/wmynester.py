"""这是”nester“模块，提供了函数print_lol()，可以打印嵌套列表"""
def print_lol(the_list):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
