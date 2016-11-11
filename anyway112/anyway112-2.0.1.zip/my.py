def shuchu(a,num):
    for b in a:
        if isinstance(b,list):
            shuchu(b,num+1)
        else:
            for tab in range(num):
                print('\t',end='')
            print(b)