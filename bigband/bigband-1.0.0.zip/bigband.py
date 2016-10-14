'''这是“form.py”模块，提供了一个名为form()的函数，这个函
数的作用是打印列表，其中有可能含有（也可能不包含）嵌套列表。'''
def form(anylist):
    '''这个函数取一个位置参数，名为“anylist”，这可以是任何
    python列表（也可以是包含嵌套列表的列表）。所指定的列表中每个
    数据项会（递归地）输出到屏幕上，各数据项各占一行。'''
    for each in anylist:
        if isinstance(each,list):
            form(each)
        else:
             print(each)
