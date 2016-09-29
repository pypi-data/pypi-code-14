import heapq

from collections import defaultdict


class FactoryClosed(Exception):
    pass


class NestedGenomicIntervalFactory:

    __slots__ = ('tops', 'parents', 'children', 'start', 'closed')

    def __init__(self):
        self.tops = []
        self.parents = {}
        self.children = defaultdict(list)
        self.start = 0
        self.closed = False

    def add_interval(self, interval, *, parents=None):
        if self.closed:
            raise FactoryClosed

        if interval.data['name'] in self.children:
            interval.children = self.children[interval.data['name']]
            del self.children
        self.parents[interval.data['name']] = interval
        if parents is None:
            heapq.heappush(self.tops, (interval.stop, interval))
        else:
            for parent in parents:
                if parent in self.parents:
                    self.parents[parent].children.append(interval)
                else:
                    self.children[parent].append(interval)
        self.start = interval.start

    def has_complete_interval(self):
        return len(self.tops) > 0 and (self.start > self.tops[0][1].stop or self.closed)

    def get_complete_interval(self):
        stop, interval = heapq.heappop(self.tops)
        del self.parents[interval.data['name']]
        return interval

    def close(self):
        self.closed = True

    def drained(self):
        return self.closed and len(self.tops) == 0

    def __getstate__(self):
        return self.tops, self.parents, self.children, self.start

    def __setstate__(self, state):
        self.tops, self.parents, self.children, self.start = state
