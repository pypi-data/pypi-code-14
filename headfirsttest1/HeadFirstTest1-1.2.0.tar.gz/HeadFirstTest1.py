# movies = ['The Holy Grail', 'The life of Brian','The meaning of life']
# movies.insert(1,1975)
# movies.insert(3,1979)
# movies.insert(5,1983)
# print(movies)


#isinstance 的测试 isinstance(变量名,类型名) 返回的是bool
#movies = ['mingzi',1975,'director',91,['main actor',['peijiao1','peijiao2'],'main actor2']]
# for printmovies in movies:
#     if isinstance(printmovies,list):
#         for neibuxunhuan1 in printmovies:
#             if isinstance(neibuxunhuan1,list):
#                 for neibuxunhuan2 in neibuxunhuan1:
#                     print(neibuxunhuan2)
#             else:
#                 print(neibuxunhuan1)
#     else:
#         print(printmovies)


#测试函数递归  递归遍历多层次列表嵌套的所有列表项
def printdigui(print_list,level = 0):
    for inside_list in print_list:
        if isinstance(inside_list,list):
            printdigui(inside_list,level+1)
        else:
            for suojin in range(level):
                print('\t',end = '')
            print('Level',level,inside_list)
    return

#movies = ['mingzi',1975,'director',91,['main actor',['peijiao1','peijiao2'],'main actor2']]
#printdigui(movies,0)
