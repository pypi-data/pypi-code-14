# -*- coding: utf-8 -*-


###
# Stack container based on a list for its internal storage
#
class Stack:
    """
    >>> s = Stack()
    >>> s.isEmpty()
    True
    >>> s.push(1)
    >>> s.push(2)
    >>> s.top()
    2
    >>> s.size()
    2
    >>> s.pop()
    2
    >>> s.top()
    1
    >>> s.size()
    1
    """
    def __init__(self):
        self.internalList = list()

    def isEmpty(self):
        return len(self.internalList) == 0

    def pop(self):
        return self.internalList.pop() if len(self.internalList) != 0 else None

    def push(self, element):
        self.internalList.append(element)

    def top(self):
        return self.internalList[-1] if len(self.internalList) != 0 else None

    def size(self):
        return len(self.internalList)

