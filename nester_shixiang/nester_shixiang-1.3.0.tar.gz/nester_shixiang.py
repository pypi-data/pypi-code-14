"""这是“wester.py”模块，提供了一个名为print_lol的函数，
这个函数的作用是打印列表，其中可能包含（也可能不包含）列表"""
def print_lol(the_list, indent = False, level = 0):
    """这个函数取一个位置参数，名为“the_list”，这可以是任何Python列表
    所指定的列表中的每个数据项会递归地输出到屏幕上，各数据项各占一行
    第二个参数indent用来设定默认是否插入制表符，缺省为False
    第三个个参数level用来在遇到嵌套列表时插入制表符,缺省为0"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
               for tab_top in range(level):
                   print('\t', end='')
            print(each_item)
