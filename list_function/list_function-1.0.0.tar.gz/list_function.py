'''
this is a function that called print_list()
which print lists which may or may not contian nested lists.
'''

'''myList=movies = [
    "The Holy Grail",
    1975,
    "Terry Jones & Terry Gilliam",
    91,
    ["Graham Chapman",
     ["Michael Palin", "John Cleese","Terry Gilliam", "Eric Idle",
      ["abc","defg","highk","Terry Jones"]
    ]
    ]
]
'''

#print(isinstance(len(myList),list))

'''
recursively print the list to screen
'''
def print_list(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_list(each_item)
        else:
            print(each_item)

#print_list(myList)