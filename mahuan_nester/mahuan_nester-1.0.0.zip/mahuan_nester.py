"""这是nester模块，提供了一个名为print_lol()的函数，这个函数的作用是打
印列表，其中有可能包含（也可能不包含）嵌套列表"""
def print_lol(the_list):
	"""这个函数取了一个位置参数，名为"the_list"，这可以是任何python列
	表（也可能是包含嵌套列表的列表）。所指定的列表中的每个数据项会（
	递归的）输出到屏幕上，各数据项各占一行"""
	for deep_the_list in the_list:
		if isinstance(deep_the_list,list):
			print_lol(deep_the_list)
		else:
			print(deep_the_list)