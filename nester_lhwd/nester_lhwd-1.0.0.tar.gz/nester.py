def nested_item(now_item):
    for each_item in now_item:
        if(isinstance(each_item,list)):
            nested_item(each_item)
        else:
            print(each_item)