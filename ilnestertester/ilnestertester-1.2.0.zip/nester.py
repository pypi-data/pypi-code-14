"""Module nester.py provides one function print_lol which prints
lists which may or may not be nested"""

def print_lol(the_list,level=0):
    """Function takes argument "the list" which is any list nestes
or not.  It also takes the argument "level" which is the number of tab
indents  the list should have.  Each item in the list is printed on screen onn it's own
line."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
