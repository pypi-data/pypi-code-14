""" 这是一个headfirst例子，学习如何建立一个迭代函数"""
def print_lol(the_list):
        """这是迭代的主体代码"""
        for each_item in the_list:      #这是循环主体
                if isinstance(each_item,list):
                        print_lol(each_item)
                else:
                        print(each_item)
