#This code makes it so that you can iterate through nested or very deeply nested lists

def print_lol(the_list, indent = False, level = 0):

	#The function iterates through the given list and then checks whether that item is a list and if it is,
	#then it will go through the list again. Otherwise, it will just print the item. The level indicates how many
	#indents each nested list will display

    for an_item in the_list:
        if isinstance(an_item, list):
            print_lol(an_item, indent,level+1)
        else:
            if indent:
                for indents in range(level):
                    print("\t", end="")
            print(an_item)

movies = ["The Holy Grail", 1975, "Terry Gilliam", 91,
            ["Graham Chapman",
                ["Micheal Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]

print_lol(movies)