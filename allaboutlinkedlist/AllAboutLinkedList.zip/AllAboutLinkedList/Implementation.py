'''
the node Implementation:
declaration: nodes node_name=Node(value,next node)
have 4 internal functions:
1.sn-set a new next node
2.sd-set a new data
3.gn-get a pointer to the next node
4.gd-# get node's data
'''

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        # print("Node created")

    def sn(self, newnext):
        self.next = newnext

    def sd(self, newdata):
        self.data = newdata

    def gn(self):
        return self.next

    def gd(self):
        return self.data


'''
the linked list implementation:
declaration:list_name=LinkedList(head)
there are internal functions:
1.isempty() - 0 if empty,1 else.
2.addnode(data) - insert node to the beginnig of the list.
3.insertnode(place,data) - insert the node in the "place" position
4.printlist() - printing the list
5.deletenode(place) - deletes a node in a the k'th place
6.size() - returns the size of the list
7.lastnode() - return a pointer to the last node in the list
8.mf(steps) - returns a pointer "steps" steps after the head pointer

'''
class LinkedList:
    def __init__(self):
        self.head = None

    def isempty(self):
        return self.head == None

    def addnode(self, data):
        tmp = Node(data)
        tmp.sn(self.head)
        self.head = tmp

    def insertnode(self, place, data):
        i = 0
        cur = self.head
        while i < (place - 2):
            cur = cur.gn()
            i += 1
        tmp = Node(data)
        tmp.sn(cur.gn())
        cur.sn(tmp)

    def printlist(self):
        cur = self.head
        print("head->", end=" ")
        while cur is not None:
            print("%d ->" % cur.gd(), end=" ")
            cur = cur.gn()
        print("None")

    def deletenode(self, place):
        cur = self.head
        i = 0
        while i < (place - 2):
            cur = cur.gn()
            i = i + 1
        cur.sn((cur.gn()).gn())


    def size(self):
        i = 0
        cur = self.head
        while cur is not None:
            cur = cur.gn()
            i = i + 1
        return int(i)

    def lastnode(self):
        cur = self.head
        while cur.gn() is not None:
            cur = cur.gn()
        end = cur
        return end

    def mf(self, steps):
        cur = self.head
        i = 0
        while i < steps:
           if cur.gn is None or cur is None:
               print("your out of the list,i can not go so far")
               return 0
           else:
                cur = cur.gn()
                i += 1
        return cur