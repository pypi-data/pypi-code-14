'''this module includes a fuction that is used to print list,and inserted lists are also useful'''

def print_lol(alist,sign=False,level=0):
    for i in alist:
        if (isinstance(i,list)):
            print_lol(i,sign,level+1)
        else:
            if sign:
                for j in range(level):
                    print "\t",
            print i
              
            
               
                

                    
               
    
           

            
