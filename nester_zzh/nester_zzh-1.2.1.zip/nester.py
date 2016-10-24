"""
2016年9月20日
这是个递归的函数，传入列表，判断有无子列表，打印输出，
这是head first pyhon 里的作业。
2016年9月21日
增加tab_size参数，控制嵌套列表打印时制表符的显示。
小于等于0时不显示制表符，大于0时显示相应数量的制表符。
2016年9月23日
增加is_usetab参数，标识是否使用缩进特性。并将后两个参数修改增加了默认值

"""
def sub_list_print(sub_list,is_usetab=False,tab_size=0):
    """函数"""
    for each_item in sub_list:
        if (isinstance(each_item,list)):
            sub_list_print(each_item,is_usetab,tab_size+1)
        else:
            #这也是个注释
            if is_usetab:
                for num_tab in range(tab_size):
                   print("\t",end='')
            print(each_item)
