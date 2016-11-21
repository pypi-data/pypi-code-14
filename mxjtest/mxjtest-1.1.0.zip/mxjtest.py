""" 这是一个headfirst例子，学习如何建立一个迭代函数"""
def print_lol(the_list,level):
        for each_item in the_list:      #这是循环主体
                if isinstance(each_item,list):
                        print_lol(each_item,level+1)
                else:
                        for tab_stop in range(level):
                                print("\t",end='')
                        print(each_item)
                        
