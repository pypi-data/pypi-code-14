"""
This is a funcition defined in order to print all of the item of the lists, even the list contains list as a item.
"""



def print_lol(the_list,num):
    """
    Read item from a list
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,num+1)
        else:
            for i in range(num):
                print ('\t',end='')
            print (each_item)
