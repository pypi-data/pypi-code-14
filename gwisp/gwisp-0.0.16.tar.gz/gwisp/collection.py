from pymongo import ASCENDING


class CollectionSpec(object):
    '''
    Contains information of index of mongodb collection

    :param str name: Name of collection
    '''
    def __init__(self, name):
        self._name = name
        self._indexes = {}

    @property
    def name(self):
        '''
        :return: Name of collection
        :rtype: str
        '''

        return self._name

    @property
    def indexes(self):
        '''
        :return: Dictionary contains pair ``str``-> ``bool``.
            Key is index name, value is dictionary contains
            ``key`` and ``unique`` key
        :rtype: dict
        '''

        return self._indexes

    def add_index(self, key, unique):
        '''
        Add an index to collection

        :param list key: List of string make a key
        :param bool unique: Mark key is unique
        '''

        self._indexes['_'.join(key)] = {
            'key': [(k, ASCENDING) for k in key],
            'unique': unique
        }

#: Password collection specification
password = CollectionSpec('password')

#: Account collection specification
account = CollectionSpec('account')
account.add_index(['name'], True)
account.add_index(['subject'], True)


#: Scheduler collection specification
scheduler = CollectionSpec('scheduler')
scheduler.add_index(['name'], True)

#: List of collection specifications in database
specs = [password, account, scheduler]
