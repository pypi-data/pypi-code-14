def print_lol (the_list , level = 0):
        for item_in_list in the_list:
                if (isinstance (item_in_list , list )):
                        print_lol (item_in_list , level + 1)
                else :
                        for n in range(level):
                                print("\t" , end='')
                        print (item_in_list)

