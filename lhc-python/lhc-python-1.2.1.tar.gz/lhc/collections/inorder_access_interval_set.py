from bisect import bisect_right
from itertools import chain


class InOrderAccessIntervalSet(object):
    def __init__(self, iterator, set_key=None, query_key=None):
        self.starts = []
        self.stops = []
        self.buffer = []

        self.iterator = iterator
        self.set_key_fn = default_key_function if set_key is None else set_key
        self.query_key_fn = default_key_function if query_key is None else query_key

    def fetch(self, *args):
        """
        Fetch the items within the given interval. The start of the given interval must be greater than or equal to the
        start of the previously used interval. The number of arguments must be equal to the number of dimensions + 1.
        The second last argument is the start position in the last dimension and the last argument is the stop position
        in the last dimension.

        :param args: interval to retrieve
        :return: list of items from the iterator
        """
        start = self.query_key_fn(args[0] if len(args) == 2 else args[:-1])
        stop = self.query_key_fn(args[1] if len(args) == 2 else (args[:-2] + args[-1:]))

        for item in self.iterator:
            key = self.set_key_fn(item)
            if key.start >= stop:
                self.iterator = chain([item], self.iterator)
                break
            index = bisect_right(self.stops, key.stop)
            self.starts.insert(index, key.start)
            self.stops.insert(index, key.stop)
            self.buffer.insert(index, item)

        cut_index = 0
        while cut_index < len(self.stops) and self.stops[cut_index] <= start:
            cut_index += 1
        self.starts = self.starts[cut_index:]
        self.stops = self.stops[cut_index:]
        self.buffer = self.buffer[cut_index:]

        return sorted(item for item_start, item in zip(self.starts, self.buffer) if item_start < stop)


def default_key_function(x):
    return x
