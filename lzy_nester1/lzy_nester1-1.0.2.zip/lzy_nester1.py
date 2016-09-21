def print_item(the_list, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_item(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end=' ')
            print(each_item)


##cast = ['palin', 'cleese', 'idle', 'jones', 'gilliam', ['chaoman',['caocao', 'lzy', 'lele']]]
##print_item(cast, 1)
