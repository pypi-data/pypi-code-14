"""这个模块提供了一个函数，作用是打印列表嵌套"""
def print_lol(thelist,level=0):
    """函数输入一个参数thelist,可以是任何python列表"""
    for theitem in thelist:
        if isinstance(theitem,list):
            print_lol(theitem,level+1)
        else:
            for num in range(level):
                print('\t',end='')
            print(theitem)
