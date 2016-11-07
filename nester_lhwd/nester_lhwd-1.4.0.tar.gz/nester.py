def nested_item(now_item,level = 0,open = True):
    for each_item in now_item:
        if(isinstance(each_item,list)):
            nested_item(each_item,level+1,open)
        else:
            if (open==True):
                print('\t' * level,end='')
            print(each_item)