name = input('what is your name?')
if name.endswith('li'):
  print ('hellow,LiDage')
else:
  print('hellow you')

#movies=['从你的全世界路过', 2017, '导演：张一白&编剧：张嘉佳', ['邓超', '张天爱', ['一点也不好看', '恩，有点坑']]]

#这是一个列表读取函数，包含列表中嵌套的列表，每个项目都可以读出

  #增加一个level变量  用于输出缩进字符tab
def nest_loop(para,level=0):
  if isinstance(para,list):
    for each_one in para:
      nest_loop(each_one,level+1)
  else:
       for num in range(level):
         print("\t",end='')
       print(para)


#print(movies)
'输出每个条目'#3个单引号对 或者 1个单引号对 都可以作为注释
#nest_loop(movies)

    
