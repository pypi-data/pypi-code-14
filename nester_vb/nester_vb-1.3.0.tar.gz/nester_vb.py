
"""This is the 'nester.py' module, and it provides one function called 
'print_lol()', which prints lists that may or may not include nested lists"""

def print_lol(the_list, indent = False, level = 0):

    """This function takes a positional argument 'the_list', which is any 
    Python list (of, possibly, nested lists). Each data item in the provided list
    is (recursively) printed to the screen on its own line. A second argument 'indent'
    allows indentation to be turned on or off. A third argument 'level'
    is used to insert tab-stops when a nested list is encountered."""
    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1)
        else:
            for tab_stop in range(level):
                if indent:
                    print("\t", end='')
            print(each_item)

