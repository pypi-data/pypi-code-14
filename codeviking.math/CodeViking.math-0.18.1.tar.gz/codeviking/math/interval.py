from collections import namedtuple


class RI(namedtuple('RI', 'min max')):
    """
    Real Interval

    .. py:method:: __new__

    .. py:attribute:: min

        lower bound.

    .. py:attribute:: max

        upper bound.

    .. describe:: x in interval

        Determine if x lies inside interval: min <= x <= max
    """

    @property
    def length(self):
        """        length of this interval"""
        return self.max - self.min

    def __contains__(self, v):
        return self.min <= v <= self.max

    def expand(self, item):
        """
        return a RI that contains both this box and item.

        :param item: can be either a RI, or a tuple of length 2
        """
        if isinstance(item, RI):
            return RI(min(self.min, item.min), max(self.max, item.max))
        if isinstance(item, tuple):
            return RI(min(self.min, item[0]), max(self.max, item[1]))

        if item in self:
            return self
        if self.is_empty:
            return RI(item, item)
        return RI(min(self.min, item), max(self.max, item))

    @property
    def is_empty(self):
        """
        return True if this interval is empty.
        """
        return self.min > self.max

    @property
    def length(self):
        """
        return length of the interval
        """
        return self.max - self.min

    def intersects(self, other):
        """
        Return True if self and other intersects.
        """
        if not isinstance(other, RI):
            other = RI(*other)
        if self.is_empty or other.is_empty:
            return False
        r = [(self.min, 0), (self.max, 0), (other.min, 1), (other.max, 1)]
        r.sort()
        return r[0][1] != r[1][1]

    def intersection(self, other):
        """
        Compute the intersection of self and other.
        """
        if not isinstance(other, RI):
            other = RI(*other)
        if not self.intersects(other):
            return self.__class__.empty
        return RI(max(self.min, other.min), min(self.max, other.max))

    def alpha(self, value):
        return (value - self.min) / self.length

    def interpolate(self, alpha):
        return self.min + alpha * self.length

    def constrain(self, value):
        return max(self.min, min(self.max, value))

    def __eq__(self, other):
        return self.min == other[0] and self.max == other[1]


RI.empty = RI(float("inf"), float("-inf"))
