"""列表（包含嵌套列表）内容依次输出模块"""
def print_list(the_list):
    """列表输出函数"""

    for each_item in the_list:
        if isinstance(each_item,list):
            print_list(each_item)
        else:
            print(each_item)

