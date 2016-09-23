def print_lol(the_list,intent = 1,level = 0):
    for item in the_list:
        if isinstance(item,list):
            print_lol(item,intent,level+1)
        else:
            if intent == 0:
                print '\t'*level,item  
            else:
                print item