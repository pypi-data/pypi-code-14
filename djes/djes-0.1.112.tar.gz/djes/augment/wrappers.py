import six


class SearchWrapper(object):

        def __init__(self, search, validators=[]):
            self.search = search
            self._exhausted = False
            self._validators = self.check_validators(validators)

        def next(self):
            return six.next(self.search)

        def __next__(self):
            return self.next()

        def check_validators(self, validators):
            if not isinstance(validators, list):
                raise TypeError('''SearchWrapper validators must be passed in as a list.''')
            for vldtr in validators:
                if not callable(vldtr):
                        raise TypeError('''SearchWrapper validators must be callable.''')
            return validators

        def is_priority(self, *args):
            for validator in self._validators:
                vld = validator(*args)
                if not isinstance(vld, bool):
                    raise TypeError('''SearchWrapper validators must return a value of type `bool`''')
                elif vld:
                    return vld
            return False
