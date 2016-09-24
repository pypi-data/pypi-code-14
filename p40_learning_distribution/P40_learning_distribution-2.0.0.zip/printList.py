#coding = utf-8

#学习创建模块
#create a module

"""
#Store lists within lists
movies =[
    "The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91,
#       movies[0],  movies[1],      movies[2],          movies[3],
        ["Graham Chapman",
#           movies[4][0]
             ["Michael Palin", "John Cleese",   "Terry Gilliam",    "Eric Idle",    "Terry Jones"   ]]]
#             movies[4][1][0], movies[4][1][1],  movies[4][1][2],   movies[4][1][3], movies[4][1][4]
#           |<------------------------- movies[4][1] ---------------------------------------------->|
#       |<------------------------------------- movies[4] ------------------------------------------->|
#    |<----------------------------------------------- movies ----------------------------------------->|
#print( movies )
"""


# def function_name ( argument(s) ):
#   function code suite
def print_lol( the_list, indent=False, level=0 ): #....给新的入口参数添加一个缺省值
                                                  #....这样就可以兼容上一个版本的函数
                                                  #....第三版加入 indent，兼容最初始无缩进                                                    
    for each_item in the_list:
        
        if isinstance( each_item, list ):
            print_lol( each_item, indent, level+1 ) #..更新indent
        else:
            if indent: #...............................更新判断是否有缩进需求
                for tab_stop in range( level ):
                    print( '\t', end = ' ' ) #.........因为print()会默认输出后
                                             #.........换行，而此处只需要Tab即可
            print( each_item )
        #end if each_item=list and else
            
    #end for the_list            
#end def function

"""
#输出列表...
print_lol( movies )
"""
#以上已经利用了 函数 和 递归

