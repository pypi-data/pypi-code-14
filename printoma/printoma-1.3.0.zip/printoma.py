def print_everything (nested_list, indent =False level=0):
    for each_item in nested_list:
        if isinstance (each_item, list):
             print_everything (each_item, level+1)  
        else:
            if indent:
                
                for each_numb in range(level):
                print ("\t", end='')

            else:
                print (each_item)
            
                   
            
