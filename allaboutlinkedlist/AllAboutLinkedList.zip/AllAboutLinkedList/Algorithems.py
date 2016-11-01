'''
I added four functions that could be used to work with linked list:
1.listintersection(list1,list2) - this function recive two linke lists and checks
if in some point they intersect, if the do, she will return a pointer
to the node they intersect
2.sort(list) - sorting the linked list.
3.reverselist(list) - reverse the list, and returns a new list
4.detectloop(list) - this function check if there is a loop in the list, if there is one
she'll return the a pointer to the node that begins the loop.
*this function is using loopstart(list,onestep) function
'''
def sort(list):
    i = 1
    j = 0
    s = list.size()
    while i < s :
        j = i - 1
        num = (list.mf(i)).gd()
        while j >= 0 and (list.mf(j)).gd() > num:
            (list.mf(j + 1)).sd(list.mf(j).gd())
            j -= 1
        (list.mf(j + 1)).sd(num)
        i += 1

def reverselist(list):
    prev=None
    cur=None
    next=list.head
    while next :
        cur=next
        next=cur.gn()
        cur.sn(prev)
        prev=cur
    head=cur
    list.head=head
    return list


# this function will get to linked list and will check if they meet, if they do, it'll return the node of the intersection
def listintersection(list1, list2):
    end1 = list1.lastnode()
    end2 = list2.lastnode()
    size1 = list1.size()
    size2 = list2.size()
    if end1 is not end2:
        print("there is no intersection between those lists")
        return 0
    else:
        size = size1 - size2
        if size >= 0:
            cur1 = list1.mf(size)
            cur2 = list2.head
        else:
            cur2 = list2.mf(abs(size))
            cur1 = list1.head
    while cur1 is not cur2:
        cur1 = cur1.gn()
        cur2 = cur2.gn()
    inode = cur1  # the node of the intersection
    return inode



#internal function of "detectloop"
def loopstart(list,onestep):
    twostep = onestep
    onestep=list.head
    counter=1
    while onestep is not twostep:
        onestep = onestep.gn()
        twostep = twostep.gn()
        counter+=1
    print("the node with the data",onestep.gd()," is the node that start the loop","and he is node number",counter)
    return onestep


def detectloop(list):
    if list.head is None:
        print("print list is empty")
        return 0
    onestep = list.head
    twostep = list.head
    while twostep is not None :
        onestep=onestep.gn()
        if list.mf(2):
            twostep = (twostep.gn()).gn()
        else:
            print("there is no loop")
            return 0
        if onestep is twostep:
            return loopstart(list, onestep)
    print("there is no loop")
    return 0
