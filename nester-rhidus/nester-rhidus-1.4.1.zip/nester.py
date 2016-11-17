"""This is the "nester.py" module and it provides one function called print_lol()
   which prints lists that may or may not include nested lists."""

import sys

def print_lol(the_list, indent=False, level=0, file=sys.stdout):
    """Prints a list of (possibly) nested lists.

       This function takes positional argument called "the_list", which
       is any Python list (of - pissibly - nested lists). Each data item in the
       provided list is (recursively) printed to the screen on it's own line.
       A second argument called "indent" controls wheter or not indentation is
       shown on the display. This defaults to False: set it to True to switch on.
       A third argument called "level" (which defaults to 0) is used to insert
       tab-stops when a nested list is encountered.
       A fourth argument called "file" is used to specify the file to print to.
       The default is sys.stdout, so it prints to Standard Output."""
       
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1, file)
        else:
            if indent:
                print("\t" * level, end='', file=file)
            print(each_item, file=file)


