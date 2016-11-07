"""This module creates a function called extendInto which allows you to insert
multiple items into an arbirtary position in a list.  Contract with the built-in
function listname.extend(list) which places items at the end of the list."""

def extendInto(baseList, position, subList):
    subList.reverse()
    for n in subList:
        baseList.insert(position, n)

        
