#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Data Structure Binary Search Tree.
:author: Manuel Tuschen
:license: FreeBSD

License
----------
Copyright (c) 2016, Manuel Tuschen
All rights reserved.
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


from __future__ import division, absolute_import, unicode_literals, print_function


__all__ = ["bstree"]


class node:
    """
    A single tree node for binary search trees.

    Methods
    ------
    hasLeftChild() : bool
        True if there is a left child.
    hasRightChild() : bool
        True if there is a right child.
    isLeftChild() : bool
        True if is a left child itself.
    isRightChild() : bool
        True if is a right child itself.
    isRoot() : bool
        True if is the root itself.
    isLeaf() : bool
        True if is a leaf itself.
    hasAnyChildren() : bool
        True if there are any children.
    hasBothChildren() : bool
        True if there are both children.
    """
    def __init__(self, key, value, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild is not None

    def hasRightChild(self):
        return self.rightChild is not None

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,key,value,lc,rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self


class bstree:
    """
    Implementation of a binary search tree with keys lesser than the parent key
    on the left. BST su
    """

    def __init__(self):
        self.__root = None
        self.__size = 0

    def __len__(self):
        return self.__size

    def __getitem__(self, key):
        if self.__root:
            res = self.__get(key, self.__root)
            if res:
                   return res.value
            else:
                   return None
        else:
            return None

    def __setitem__(self, key, value):
        if self.__root:
            self.__set(key, value, self.__root)
        else:
            self.__root = node(key, value)
        self.__size += 1

    def __contains__(self,key):
        if self.__getitem__(key):
            return True
        else:
            return False

    def __delitem__(self, key):
        if self.__size > 1:
          nodeToRemove = self.__getitem__(key)
          if nodeToRemove:
              self.__remove(nodeToRemove)
              self.__size = self.__size-1
          else:
              raise KeyError('Key not in tree')
        elif self.__size == 1 and self.__root.__key == key:
            self.__root = None
            self.size = self.size - 1
        else:
            raise KeyError('Key not in tree')

    def __iter__(self):
        if self:
            if self.hasLeftChild():
                for elem in self.leftChiLd:
                    yield elem
            yield self.key
            if self.hasRightChild():
                for elem in self.rightChild:
                    yield elem

    def __get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self.__get(key, currentNode.leftChild)
        else:
            return self.__get(key, currentNode.rightChild)

    def __set(self, key, value, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self.__set(key,value,currentNode.leftChild)
            else:
                currentNode.leftChild = node(key,value,parent=currentNode)
        elif key < currentNode.key:
            if currentNode.hasRightChild():
                   self.__set(key,value,currentNode.rightChild)
            else:
                currentNode.rightChild = node(key,value,parent=currentNode)
        else:
            raise KeyError("Key already in use.")

    def __remove(self, currentNode):
        if currentNode.isLeaf():  # leaf
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren():  # interior
            succ = currentNode.findSuccessor()
            succ.spliceOut()
            currentNode.key = succ.key
            currentNode.payload = succ.payload
        else:  # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key, currentNode.leftChild.payload,currentNode.leftChild.leftChild, currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key, currentNode.rightChild.payload,  currentNode.rightChild.leftChild, currentNode.rightChild.rightChild)

    def __findSuccessor(self, currentNode):
        succ = None
        if currentNode.hasRightChild():
            succ = self.__findMin(currentNode.rightChild)
        else:
            if currentNode.parent:
                if currentNode.isLeftChild():
                    succ = currentNode.parent
                else:
                    currentNode.parent.rightChild = None
                    succ = currentNode.parent.findSuccessor()
                    currentNode.parent.rightChild = currentNode
        return succ

    def __findMin(self, currentNode):
      while currentNode.hasLeftChild():
          currentNode = currentNode.leftChild
      return currentNode
