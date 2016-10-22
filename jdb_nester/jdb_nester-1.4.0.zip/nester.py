"""This is the "nester.py" module, and it provides one function called
    print_lol which prints lists that may or may not include nested lists."""
import sys


def print_lol(the_list, indent=False, level=0, data=sys.stdout):
    """This function takes one positional argument called 'the_list', which
        is any Python list (of - possibly - nested lists).  Each data item in the
        provided list is (recursively) printed to the screen on it's own line.

        The second optional argument 'indent' disables the third argument.  Default is off.

        A third optional argument called 'level' is used to insert tab-stops when a nested list is encountered.
        A negative value for 'level' will turn off the indention until a positive integer is reached in nesting loops

        The last fourth argument optionally writes the inputed list to a file instead of the standard output."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, data)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t', end='', file=data)
            print(each_item, file=data)

