import sys
def nested_item(now_item,level = 0,open = True,output = sys.stdout):
    for each_item in now_item:
        if(isinstance(each_item,list)):
            nested_item(each_item,level+1,open,output)
        else:
            if (open==True):
                print('\t' * level,end='',file=output)
            print(each_item,file=output)