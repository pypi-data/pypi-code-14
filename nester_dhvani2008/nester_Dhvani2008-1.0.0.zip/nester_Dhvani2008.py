def print_lol (the_list):
        for item_in_list in the_list:
                if (isinstance (item_in_list , list )):
                        print_lol (item_in_list)
                else :
                        print (item_in_list)

