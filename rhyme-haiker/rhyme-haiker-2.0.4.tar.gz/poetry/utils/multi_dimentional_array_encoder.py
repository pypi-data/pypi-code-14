# -*- coding: utf-8 -*-

import json


class MultiDimentionalArrayEncoder(json.JSONEncoder):

    def encode(self, obj):
        def hint_tuples(item):
            if isinstance(item, tuple):
                print("item----: ", item)
                return {'__tuple__': True, 'items': item}
            if isinstance(item, list):
                return [hint_tuples(e) for e in item]
            else:
                return item

        return super(MultiDimentionalArrayEncoder, self).encode(hint_tuples(obj))


def hinted_tuple_hook(obj):
    if '__tuple__' in obj:
        return tuple(obj['items'])
    else:
        return obj

if __name__ == '__main__':
    enc = MultiDimentionalArrayEncoder()
    data = {('a', 'b', 'c'): ['A', 'B', 'C']}
    enc.encode(data)
