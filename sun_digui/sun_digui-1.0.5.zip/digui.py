#coding=utf-8
#movices=["a","b",["c","d"],"e",["f"]]
'''for index in movices:
    if isinstance(index,list):
      for index1 in index:
            if isinstance(index1,list):
                    for index2 in index1:
                        print(index2)
            else:
                     print(index1)
    else:
from aifc import data
from digui import print_list
       print(index)'''
def print_list(_list,indent=False,level=0):
    for index in _list:
     if isinstance(index,list):
          print_list(index,indent,level+1)
     else:
        if indent: 
         for tab_stop in range(level):  
           print('\t')
        print(index)
   
