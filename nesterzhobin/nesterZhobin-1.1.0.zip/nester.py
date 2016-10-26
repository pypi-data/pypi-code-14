"""
this is a nester module, and it provide a function called print_lol()
which prints lists that may or may not includ nested list
"""


def print_lol(the_list,level):
    """
     this function takes a two arguments called 'the_list' and 'level'.
     A seconed argument used to insert tab-stop when a nested list is encountered
    """
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print ('\t',end='')
            print(each_item)
