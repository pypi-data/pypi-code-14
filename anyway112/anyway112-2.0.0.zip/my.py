def shuchu(a):
    for b in a:
        if isinstance(b,list):
            shuchu(b)
        else:
            print(b)