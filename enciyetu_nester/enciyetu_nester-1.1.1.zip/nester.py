"""this is the 'nest.py' module and it provide a function called printlist().
the function can print lists that may or may not include the nested lists. 
"""
def printlist(currlist, display = False, level = 0):
    for each_item in currlist:
        if isinstance(each_item, list):
            printlist(each_item, display, level + 1)
        else:
        	if display:
        		for i in range(level):
        			print("\t", end = "")
        	print(each_item)
