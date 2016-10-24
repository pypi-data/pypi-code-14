

class Cairy(object):

    def __init__(self, incoming, outgoing):
        self.incoming = incoming
        self.outgoing = outgoing

    def merge(self, a, b, path=None, update=True):
        if path is None: path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass  # same leaf value
                elif isinstance(a[key], list) and isinstance(b[key], list):
                    for idx, val in enumerate(b[key]):
                        a[key][idx] = self.merge(a[key][idx], b[key][idx], path + [str(key), str(idx)], update=update)
                elif update:
                    a[key] = b[key]
                else:
                    raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
            else:
                a[key] = b[key]
        return a

    def json_mapper(self, incoming, outgoing):
        incoming_split = incoming.split('.')
        outgoing_split = outgoing.split('.')
        current_dict = self.data
        for key in incoming_split:
            current_dict = current_dict[key]
        current_val = current_dict

        root_dict = {}
        returning_dict = root_dict
        last_dict, last_key = None, None
        for key in outgoing_split:
            returning_dict[key] = {}
            last_dict = returning_dict
            last_key = key
            returning_dict = returning_dict[key]
        last_dict[last_key] = current_val
        return root_dict

    def transform(self, data):
        self.data = data
        a = {}
        for result in map(self.json_mapper, self.incoming, self.outgoing):
            self.merge(a, result)
        return a

