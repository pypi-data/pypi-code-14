def print_lol(the_list, indent=False, level=0):    # 是否启用缩进功能
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1)
        else:
            if indent:
                print('\t' * level, end='')  # 简化，不用循环
            print(each_item)


