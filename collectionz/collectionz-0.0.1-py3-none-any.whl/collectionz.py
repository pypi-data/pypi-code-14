from functools import reduce
from collections import defaultdict
from collections.abc import Hashable


class GroupBy:
    def __init__(self, objects, groupers):
        self._groupers = groupers
        if not self._groupers:
            self._group = objects
        else:
            add_to_group = self._build_add_to_group(self._groupers[0])
            grouped = reduce(add_to_group, objects, defaultdict(list))
            self._group = {
                bucket: GroupBy(objs, self._groupers[1:])
                for bucket, objs in grouped.items()}

    def _build_add_to_group(self, grouper):
        def add_to_group(group, obj):
            bucket = grouper(obj)
            if not isinstance(bucket, Hashable):
                error_tpl = 'Value returned by function "{}" is not hashable'
                raise Exception(error_tpl.format(grouper.__name__))
            group[bucket].append(obj)
            return group
        return add_to_group

    def process(self, processor):
        if type(self._group) is list:
            self._group = processor(self._group)
        else:
            for bucket in self._group:
                self._group[bucket].process(processor)

    def process_with(self, processor, *buckets):
        if type(self._group) is list:
            return [processor(self._group, *buckets)]
        else:
            return reduce(lambda a, b: a + b, [
                self[bucket].process_with(processor, *(buckets + (bucket,)))
                for bucket in self])

    def add(self, obj):
        self._add(obj, self._groupers)

    def _add(self, obj, groupers):
        if not groupers:
            self._group.append(obj)
        else:
            bucket = groupers[0](obj)
            self._group[bucket]._add(obj, groupers[1:])

    def add_grouper(self, grouper):
        if type(self._group) is list:
            self._group = GroupBy(self._group, [grouper])
        else:
            for bucket in self:
                self[bucket].add_grouper(grouper)

    def __getitem__(self, bucket):
        return self._group[bucket]

    def __iter__(self):
        return self._group.__iter__()

    def __len__(self):
        if type(self._group) is list:
            return len(self._group)
        else:
            return sum(map(len, self._group.values()))

    def __eq__(self, obj):
        return self._group == obj

    def __repr__(self):
        return repr(self._group)

    __str__ = __repr__


class CounterBy(GroupBy):
    def __init__(self, items, by):
        super(CounterBy, self).__init__(items, [by])
        self.process(len)
