"""
Knapsack
========
This is a dynamic programming solution to Knapsack problem.
Item is a generic class which has the required "weight" and
"value" attributes. Item takes in multiple values, from which
 the mean is calculated. The mean will then be used for
 evaluating the importance of that item. Item can be easily
 extended.
"""

import math


class Item(object):
    def __init__(self, name, weight, values):
        """Item.

        Args:
            name (str): Name of this item.
            weight (int): Weight of this item.
            values (list): list of value parameters of this item.
        """

        self._name = name
        self._weight = weight
        self._values = values

    @property
    def name(self):
        """Return name of Item.

        Return:
            str: Name of the Item.
        """

        return self._name

    @property
    def weight(self):
        """Return weight of the Item.

        Return:
            int: Weight of the Item.
        """

        return self._weight

    @property
    def value(self):
        """Return mean of the values of this Item.

        Return:
            int: Round up of the mean of the values.
        """

        return math.ceil(sum(self._values) / len(self._values))


class Knapsack(object):
    def __init__(self, capacity):
        """Create Knapsack instance

        Args:
            capacity (int): Knapsack capacity.
        """

        self._capacity = capacity

    @property
    def items(self):
        """Return items

        Return:
            list: Return list of Item objects.
        """

        return self._items

    @items.setter
    def items(self, items):
        """Set items

        Args:
            list: list of Item objects.
        """

        self._items = items

    def pick_items(self, sort_by='value', sort_descending=True):
        """Return max possible good items fit within capacity.

        Args:
            sort_by (str): sort the picked Items by desired property.
            sort_descending (bool): True for descending order.
        Return:
            list: list of filtered Item objects.
        """

        m = [[0 for j in range(self._capacity + 1)] for i in range(len(self._items))]
        for index, item in enumerate(self._items):
            for j in range(1, self._capacity + 1):
                if j < item.weight:
                    m[index][j] = m[index - 1][j]
                else:
                    m[index][j] = max(item.value + m[index - 1][j - item.weight], m[index - 1][j])

        ans = []
        i = len(self._items) - 1
        j = self._capacity
        while i > 0 and j > 0:
            if m[i][j] != m[i - 1][j]:
                ans.append(self._items[i])
                j -= self._items[i].weight
            i -= 1
        if sort_by:
            ans = sorted(
                ans,
                key=lambda item: getattr(item, sort_by),
                reverse=sort_descending)
        return ans
