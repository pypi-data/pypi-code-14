def print_lol(list_item, level = 0):
	for each_item in list_item:
		if isinstance(each_item, list):
			print_lol(each_item, level + 1);
		else:
			for num in range(level):
				print('\t', end='');
			print(each_item);

