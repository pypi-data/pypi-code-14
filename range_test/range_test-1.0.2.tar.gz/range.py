#for num in range(2):
 #   print(num)


movies = [
    "The Holy Grail",
    1975,
    "Terry Jones & Terry Gilliam",
    911111,
    ["Graham Chapman",
     ["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle",
      ["abc", "defg", "highk", "Terry Jones"]
      ]
     ]
]

movies1 =  ["The Holy Grail",1975,
            ["Terry Jones","Terry Gilliam"],
            [911111,"trdfc"]]

def print_list2(the_list,indentation=False,level=1):
    '''"""This function takes a positional argument called "the_list", which
is any Python list (of - possibly - nested lists). Each data item in the
provided list is (recursively) printed to the screen on it's own line.
the second : false or true to set default indentation
third:  paramter level is used to insert "tab" when a nested list is encountered'''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_list2(each_item,indentation,level+1)
            #print(level)

        else:
            if indentation:
                for tab_stop in range(level):
                #print("we will put a tab here")
                    print("\t", end='')
            print(each_item)




#invoke the function
#print_list2(movies,True)







