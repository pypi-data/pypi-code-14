"""This is a module that was created while
   working through "Head First Python" """

def print_lol(the_list, indent = False, level = 0):
    """This function takes positional argument called "the_list", which
       is any Python list (of - pissibly - nested lists). Each data item in the
       provided list is (recursively) printed to the screen on it's own line.
       A second argument "level" is used to insert tab-stops when a nested list
       is encountered."""
       
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1)
        else:
            if indent:
                print("\t" * level, end='')
            print(each_item)


