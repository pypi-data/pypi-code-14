"""这是nester.py模块，提供了一个print_lol函数。
这个函数的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表。
"""
def print_lol(the_list,level):
        """第一个参数为位置参数，名为the_list，它可以是任何Python列表
        所指定的列表中的每项数据都会递归显示，各数据项各占一行。
        第二个参数level用来控制遇到嵌套列表时插入的制表符数量。
        """
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item,level+1)
                else:
                        for tab_stop in range(level):
                                print("\t",end='')
                        print(each_item)



                                      
