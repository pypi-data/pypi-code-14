# -*- coding: utf-8 -*-


class Container:
    @staticmethod
    def each(cls, collection, callback):
        pass

    @classmethod
    def flatten(cls, collection):
        """
        >>> Container.flatten([[[1], 2, [3, 4]], 5, [6], [7, 8, 9]])
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        l = []
        for item in collection:
            if isinstance(item, list):
                l.extend(cls.flatten(item))
            else:
                l.append(item)
        return l

    @classmethod
    def unique(cls, collection):
        """
            >>> Container.unique([1, 2, 1, 2, 5, 3, 3, 4, 4, 1, 1, 1, 4, 5, 6, 7, 7, 6, 8, 7, 8, 9])
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
            >>> Container.unique((1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 5, 6, 7, 7, 7, 7, 7, 8, 9))
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
            >>> Container.unique(['a', 'z', 'a', 'b', 'a', 'z', 'b'])
            ['a', 'b', 'z']
        """
        return sorted(list(set(collection)))

    @classmethod
    def sameElements(cls, left, right):
        """
            >>> Container.sameElements([1, 2, 3], [3, 2, 1])
            True
            >>> Container.sameElements([1, 2, 3], [1, 2, 3, 4])
            False
        """
        s1 = set(left)
        s2 = set(right)
        if s1 == s2:
            return True
        return False

    @classmethod
    def keep(cls, collection, element):
        return list(filter(lambda x: x == element, collection))

    @classmethod
    def without(cls, collection, element):
        """
        >>> Container.without([1, 2, 3, 4, 5], 5)
        [1, 2, 3, 4]
        >>> Container.without([1, 2, 3], 2)
        [1, 3]
        """
        return list(filter(lambda x: x != element, collection))

    @classmethod
    def indexOf(cls, collection, element):
        """
        >>> Container.indexOf("Hello There", 'e')
        1
        >>> Container.indexOf([0, 2, 3], 1)
        -1
        """
        index = -1
        for item in collection:
            index += 1
            if item == element:
                return index
        return -1

    @classmethod
    def lastIndexOf(cls, collection, element):
        """
        >>> Container.lastIndexOf([1, 2, 3, 1, 5, 6, 1], 1)
        6
        >>> Container.lastIndexOf([1, 2, 3, 1, 5, 6, 1], 10)
        -1
        """
        index = -1
        while index < len(collection):
            index += 1
            if element == collection[len(collection) - index - 1]:
                return len(collection) - index - 1
        return -1
