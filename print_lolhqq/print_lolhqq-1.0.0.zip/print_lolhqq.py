def print_lol(a_list):
    for x in a_list:
        if isinstance(x,list):
            print_lol(x)
        else:
            print x
