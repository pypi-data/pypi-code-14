"""
data.single_list

An implementation of a singly linked list.
"""

class SingleList(object):
    """An implementation of a singly linked list."""

    def __init__(self, *elems):
        self.first = None
        self.last = None
        self.size = 0
        for elem in elems:
            self.push_back(elem)

    def __contains__(self, elem):
        """Is the given element in the list?"""
        return elem in iter(self)

    def __iter__(self):
        """Return an iterator through the list's elements"""
        node = self.first
        while node is not None:
            yield node.elem
            node = node.link

    def __len__(self):
        """How many elements are there in the list?"""
        return self.size

    def is_empty(self):
        """Is the list currently empty?"""
        return self.size == 0

    def peek_front(self):
        """If the list is non-empty, return the first element in the list."""
        return None if self.is_empty() else self.first.elem

    def peek_back(self):
        """If the list is non-empty, return the last element in the list."""
        return None if self.is_empty() else self.last.elem

    def pop_front(self):
        """If the list is non-empty, remove and return the first element from
        the list.
        """
        if self.is_empty():
            return
        elem = self.first.elem
        self.first = self.first.link
        self.size -= 1
        return elem

    def pop_back(self):
        """If the list is non-empty, remove and return the last element from the
        list.
        """
        if self.size < 2:
            return self.pop_front()
        elem = self.last.elem
        self.last = self.first
        while self.last.link.link is not None:
            self.last = self.last.link
        self.last.link = None
        self.size -= 1
        return elem

    def push_front(self, elem):
        """Push the given element onto the front of the list."""
        self.first = Node(elem, self.first)
        if self.is_empty():
            self.last = self.first
        self.size += 1

    def push_back(self, elem):
        """Push the given element onto the back of the list."""
        if self.is_empty():
            return self.push_front(elem)
        self.last.link = Node(elem)
        self.last = self.last.link
        self.size += 1

class Node(object):
    """The implementation of a node within the linked list."""

    def __init__(self, elem, link=None):
        self.elem = elem
        self.link = link
