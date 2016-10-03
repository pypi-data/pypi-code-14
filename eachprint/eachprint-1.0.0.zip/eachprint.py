def print_lol(items):
    for each_items in items:
        if isinstance(each_items,list):
            print_lol(each_items)
        else:
            print(each_items)
#print_lol函数可以将多层表格里的每一个项目全部输出在屏幕上。
         
    
