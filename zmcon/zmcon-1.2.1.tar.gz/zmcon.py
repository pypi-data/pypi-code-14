def printl(each_item, indent=False,level=0):

    
    for i in each_item:
        if isinstance(i,list):
            printl(i, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end='')
            print(i)
