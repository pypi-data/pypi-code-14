def printl(each_flick, level=0):

    
    for i in each_flick:
        if isinstance(i,list):
            printl(i, level+1)
        else:
            for tab_stop in range(level):
                print('\t',end='')
            print(i)
