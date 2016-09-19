"""
This is a funcition defined in order to print all of the item of the lists, even the list contains list as a item.
"""

def print_lol(the_list):
    """
    Read item from a list
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print (each_item)
