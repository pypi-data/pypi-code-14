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
def print_lol( the_list ):
    
    for each_item in the_list:
        
        if isinstance( each_item, list ):
            print_lol( each_item )
        else:
            print( each_item )
        #end if each_item=list and else
            
    #end for the_list            
#end def function

"""
#输出列表...
print_lol( movies )
"""
#以上已经利用了 函数 和 递归

