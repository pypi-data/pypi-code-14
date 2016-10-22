#This code makes it so that you can iterate through nested or very deeply nested lists

def print_lol(the_list, level = 0):

	#The function iterates through the given list and then checks whether that item is a list and if it is,
	#then it will go through the list again. Otherwise, it will just print the item. The level indicates how many
	#indents each nested list will display

    for an_item in the_list:
        if isinstance(an_item, list):
            print_lol(an_item, level+1)
        else:
            for indents in range(level):
        	    print("\t", end="")
            print(an_item)
