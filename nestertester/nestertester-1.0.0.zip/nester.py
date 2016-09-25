"""Module nester.py provides one function print_lol which prints
lists which may or may not be nested"""

def print_lol(the_list):
    """Function takes argument "the list" which is any list nestes
or not.  Each item in the list is printed on screen onn it's own
line"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
