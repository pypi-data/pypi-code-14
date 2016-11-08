"""你们都是逗逼，都没我帅"""
handsome_boy=["小明不帅",
              ["小白也不帅",
               ["龙哥真帅"]]]
def print_l(the_list):
   """我只想做个安静的美男子，可惜总有人羡慕我的颜值"""
   for each_a in the_list:
        if isinstance(each_a,list):
            print_l(each_a)
        else:
            print(each_a)
