import numpy as np
import itertools
from collections import defaultdict


def bin_index_map(bin_index):
    acc = 0
    for i in bin_index:
        acc = 2 * acc + i
    return acc


def reduce_index_table(dim, start_number=0):
    ret = [[] for i in range(2 ** dim)]
    indices = list(itertools.product([0, 1], repeat=dim))
    for num, ((numind1, arg1), (numind2, arg2)) in enumerate(itertools.permutations(enumerate(indices), 2)):
        ar1 = np.array(arg1)
        ar2 = np.array(arg2)
        bt = np.array(range(dim))[(ar1 != ar2)][0] + 1
        if (np.sum(ar1 == ar2) == dim - 1):
            ret[numind1].append((numind2 + start_number, bt if numind1 < numind2 else -bt))
    return ret


def power_of_to(num):
    return num != 0 and ((num & (num - 1)) == 0)


def ndto1d(index, shape):
    ret = 0
    for ind, sha in zip(index, shape):
        ret = ret * sha + ind
    return ret


class ndNode:
    gnumber = 0

    def __init__(self, parent, lbound, gbound, dim=1, gnumber=0):
        self.gnumber = gnumber
        self.parent = parent
        if parent is None:
            self.depth = 0
            self.dim = dim
        else:
            self.depth = parent.depth + 1
            self.dim = parent.dim
        self.children = [None] * (2 ** self.dim)  # number of children - ndim power of 2
        if self.dim == len(lbound) and self.dim == len(gbound):
            self.gbound = np.array(gbound)
            self.lbound = np.array(lbound)
        elif len(lbound) == len(gbound):
            self.gbound = np.repeat(gbound[0], repeats=dim)
            self.lbound = np.repeat(lbound[0], repeats=dim)
        else:
            raise ValueError('Watch bound arguments')
        self.size = np.min(self.gbound - self.lbound)

    def divide(self, start_number=0):
        middle = (self.lbound + self.gbound) / 2.
        bounds = np.vstack((self.lbound, middle))
        size = (self.gbound - self.lbound) / 2.
        for num, index in enumerate(itertools.product(*bounds.transpose())):
            self.children[num] = ndNode(parent=self, lbound=index, gbound=index + size, gnumber=start_number + num)


class ndTree:
    nodeList = []
    dividedList = []
    counter = 0
    connections = defaultdict(list)

    def __init__(self, rootnode, minsize=0.1, maxsize=0.5, mode='BF', index=None, if_interest_func=None):
        self.if_interest_func = if_interest_func
        self.maxsize = maxsize
        self.minsize = minsize
        self.rootnode = rootnode
        if mode == 'BF':
            self.bf_subdivide(rootnode)
        elif mode == 'DF':
            self.df_subdivide(rootnode)
        elif mode == 'BFb':
            self.bf_subdivide(rootnode, mode='WC')

    def df_subdivide(self, node):  # depth first
        node.gnumber = self.counter
        self.counter += 1
        if self.if_divide(node):
            node.divide()
            for child in node.children:
                self.df_subdivide(child)

    def bf_subdivide(self, node, mode='NC'):
        if len(self.nodeList) == 0 and len(self.dividedList) == 0:
            self.nodeList.append(node)
            self.dividedList.append(False)
            self.counter = 0
        elif len(self.nodeList) != len(self.dividedList):
            raise ValueError('It didnt mean to work like that')
        else:
            self.counter = node.gnumber

        while True:
            if self.if_divide(node) or mode == 'WC_force':
                node.gnumber = self.counter
                node.divide(start_number=len(self.nodeList))
                self.dividedList[self.counter] = True
                self.nodeList[self.counter] = node
                self.dividedList.extend([False] * len(node.children))
                self.nodeList.extend(node.children)
                if (mode == 'WC' or mode == 'WC_force'):
                    n = len(self.nodeList)
                    d = self.rootnode.dim
                    length = 2 ** d
                    for num, cs in enumerate(reduce_index_table(dim=d, start_number=n - length)):
                        self.connections[n - length + num].extend(cs)
                    self.collocate_bounds()
                    if (mode == 'WC_force'):
                        break

            self.counter += 1
            if self.counter == len(self.nodeList):
                break
            node = self.nodeList[self.counter]
            # setup logic here ######

    def if_divide(self, node):
        if node.size > self.maxsize:
            return True
        else:
            if node.size > self.minsize:
                if (self.if_interest(node)):
                    return True
                else:
                    return False
            else:
                return False

    def if_final_size(self, node):
        if (node.size <= self.minsize):
            return True
        else:
            return False

    def if_interest(self, node):
        if (self.if_interest_func is None):
            mid = (node.lbound + node.gbound) / 2.
            powmid = np.sum(np.square(mid))
            return (np.sin(np.sqrt(powmid) * np.pi) > 0.9) or (np.cos(np.sqrt(powmid + 1.0) * np.pi) > 0.9)
        else:
            return self.if_interest_func(node)

    ########################
    def collocate_bounds(self):  # private usage only
        dim = self.rootnode.dim
        n = len(self.nodeList)
        length = 2 ** dim
        indices = list(itertools.product([0, 1], repeat=dim))
        for num, cs in enumerate(self.connections[self.counter]):
            for numind, i in enumerate(indices):
                if ((i[np.abs(cs[1]) - 1] == 0 and cs[1] < 0) or (i[np.abs(cs[1]) - 1] == 1 and cs[1] > 0)):
                    if self.if_bordered(divided_node=self.nodeList[n - length + numind], \
                                        bordered_node=self.nodeList[cs[0]], overthrow_axis=np.abs(cs[1])):
                        self.connections[n - length + numind].append((cs[0], cs[1]))
                        self.connections[cs[0]].append((n - length + numind, -cs[1]))
                    if (self.counter, -cs[1]) in self.connections[cs[0]]:
                        self.connections[cs[0]].remove((self.counter, -cs[1]))

    def if_bordered(self, divided_node, bordered_node, overthrow_axis):
        ret = True
        dim = divided_node.dim
        for i in range(dim):
            tmp = False
            if (i != overthrow_axis - 1):
                tmp = tmp or (
                    divided_node.lbound[i] >= bordered_node.lbound[i] and divided_node.lbound[i] <=
                    bordered_node.gbound[i])
                tmp = tmp or (
                    divided_node.gbound[i] <= bordered_node.gbound[i] and divided_node.gbound[i] >=
                    bordered_node.lbound[i])
                ret = ret and tmp
        return ret

    def balance(self):
        for key, connection in dict(self.connections).items():
            if (not self.dividedList[key]) and (not self.if_final_size(self.nodeList[key])):
                for c in connection:
                    if self.if_interest(self.nodeList[key]) or \
                            ((not self.dividedList[c[0]]) and (
                                            self.nodeList[c[0]].depth - self.nodeList[key].depth > 1)):
                        self.bf_subdivide(self.nodeList[key], mode='WC_force')
                        break

    def num__of_nodes(self):
        count = 0
        for boo, i in zip(self.dividedList, self.nodeList):
            if not boo:
                count += 1
        return count
