# MIT License

# Copyright (c) 2016 Diogo Dutra

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from zlib import decompress
import numpy as np


class FilterBaseBy(object):

    def __init__(self, items_model, name, is_inclusive, id_name=None):
        self.key = items_model.__key__ + '_' + name + '_filter'
        self.items_model = items_model
        self.name = name
        self.is_inclusive = is_inclusive
        self.id_name = id_name

    def filter(self, session, rec_vector):
        filter_ = session.redis_bind.get(self.key)
        if filter_ is not None:
            filter_ = self._prepare_filter(filter_, rec_vector.size)
            self._filter(filter_, rec_vector)

    def _prepare_filter(self, filter_, new_size):
        return self._resize_vector(np.fromstring(decompress(filter_, new_size)))

    def _resize_vector(self, vector, new_size):
        if vector.size != new_size:
            vector.resize(new_size, refcheck=False)

    def _filter(self, filter_, rec_vector):
        if not self.is_inclusive:
            filter_ = np.invert(filter_)

        if np.sum(filter_):
            rec_vector *= filter_


class BooleanFilterBy(FilterBaseBy):
    pass


class MultipleFilterBy(FilterBaseBy):

    def filter(self, session, rec_vector, ids):
        filters = session.redis_bind.hmget(self.key, *ids)
        filters = [self._prepare_filter(filter_. rec_vector.size)
                    for filter_ in filters if filter_ is not None]
        final_filter = np.zeros(rec_vector.size, dtype=np.bool)

        for filter_ in filters:
            final_filter = np.logical_or(final_filter, filter_)

        self._filter(final_filter, rec_vector)


class SimpleFilterBy(MultipleFilterBy):
    pass


class ObjectFilterBy(MultipleFilterBy):

    def _get_id_from_property(self, item):
        return item[self.name][self.id_name]


class ArrayFilterBy(MultipleFilterBy):
    pass


class SimpleFilterOf(SimpleFilterBy):

    def filter(self, session, rec_vector, items_ids):
        items = self.items_model.get(session, items_ids)
        filter_ids = [item[self.name] for item in items]
        SimpleFilterBy.filter(self, session, rec_vector, filter_ids)


class ObjectFilterOf(ObjectFilterBy):

    def filter(self, session, rec_vector, items_ids):
        items = self.items_model.get(session, items_ids)
        filter_ids = [self._get_id_from_property(item) for item in items]
        ObjectFilterBy.filter(self, session, rec_vector, filter_ids)


class ArrayFilterOf(ArrayFilterBy):

    def filter(self, session, rec_vector, items_ids):
        items = self.items_model.get(session, items_ids)
        filter_ids = []
        [filter_ids.extend(item[self.name]) for item in items]
        ArrayFilterBy.filter(self, session, rec_vector, filter_ids)
