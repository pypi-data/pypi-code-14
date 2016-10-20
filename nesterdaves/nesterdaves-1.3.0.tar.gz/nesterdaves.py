"""This is the "nester.py" module and it provides one function called print_lol() 
   which prints lists that may or may not include nested lists."""

def print_lol(the_list, indent=False, level=0):
    """This function takes one positional argument called "the_list", which
       is any Python list (of -possibly- nested lists). Each data item in the
       provided list is (recursively) printed to the screen on it's own
       line.
       A second argument called "indent" is used to enable/disable indentation
       A third argument called "level" is used to insert tab-stops when a
       nested list is encountered"""

    for item in the_list:
        if isinstance(item, list):
            print_lol(item, indent, level+1)
        else:
            if indent:
                for i in range(level):
                    print("\t", end='')
            print(item)
