#coding=utf-8
#movices=["a",10,"b",20,["c",30,"d",40,["e",50,"f",60]]]
'''for index in movices:
    if isinstance(index,list):
      for index1 in index:
            if isinstance(index1,list):
                    for index2 in index1:
                        print(index2)
            else:
                     print(index1)
    else:
       print(index)'''
def print_list(_list,level):
    for index in _list:
        if isinstance(index,list):
          print_movices(index,level+1)
        else:
         for tab_stop in range(level):  
            print("\t\n")
        print(index)
      
