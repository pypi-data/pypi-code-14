def print_lol (the_list , indent = False , level = 0):
        for item_in_list in the_list:
                if (isinstance (item_in_list , list )):
                        print_lol (item_in_list , indent , level + 1)
                else :
                        if indent :
                                for n in range(level):
                                        print("\t" , end='')
                        print (item_in_list)

