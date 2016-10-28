def CD(alist,level):
	for each_item in alist:
		if isinstance(each_item,list):
			CD(each_item,level+1)
		else:
			for tab_stop in range(level):
				print("\t\n")
			print(each_item)
