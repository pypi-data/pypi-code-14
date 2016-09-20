##x = 15
##if (x/2)*2 == x:
##     print ('Even')
##else: print ('Odd')

##for each_item in movies:
##    if isinstance(each_item, list):
##        for each1_item in each_item:
##            if isinstance(each1_item, list):
##                for each2_item in each1_item:
##                    print (each2_item)
##            else:
##                print (each1_item)
##    else:
##        print (each_item)

"""循环"""
def  print_item(the_list):
    for each_item in the_list:
        if isinstance(each_item, list):
            """循环"""
            print_item(each_item)
        else:
                print (each_item)





