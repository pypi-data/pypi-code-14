def nested_item(now_item,level1=0):
    for each_item in now_item:
        if(isinstance(each_item,list)):
            nested_item(each_item,level1+1)
        else:
            for num in range(level1):
                print('\t',end='')
            print(each_item)