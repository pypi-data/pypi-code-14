# encoding: utf-8

class Persist(object):

    """
    Add a key value pair to persistent storage
    e.g. to a database table given appropriate methods.

    The 'persistent store' needs to implement __getitem__ and set.
    """
    def __init__(self,
                 persistent_store,
                 identifier,
                 identifier_key = u'parameter',
                 initial_value = u'',
                 value_key = u'value',
                 **default_parameters):
        """

        :param persistent_store: An object that gives access to the persistent
                                 store. It should implement __getitem__, raising
                                 KeyError if the item is not found. It should

        :param identifier: Name of thing we are storing, e.g. username
        :param identifier_key: formal parameter for the identifier in the
                               persistent store's set method
        :param initial_value: Set this value in the persistent store if it's
                              not there already
        :param value_key: formal parameter for the value in the persistent
                          store's set method
        :param default_parameters: If there are additional default parameters
                                   required by the set method, add them as
                                   names parameters in init. For non-default
                                   additional parameters, add them to the call
                                   to Persist's set method
        """
        self.persistant_store = persistent_store
        self.identifier = identifier
        self.identifier_key = identifier_key
        self.initial_value = initial_value
        self.value_key = value_key
        self.default_parameters = default_parameters

    @staticmethod
    def encode(self):
        """
        Overload this if you need to modify the value before storing
        e.g. Pickle
        """
        pass

    @staticmethod
    def decode(self):
        """
        Overload this if you need to modify the value after retrieving
        e.g. Unpickle
        """
        pass

    def set(self,
            value,
            **params):
        all_params = {}
        all_params.update(self.default_parameters)
        all_params.update(params)
        all_params.update({self.identifier_key: self.identifier,
                           self.value_key:      value})
        self.persistant_store.set(**all_params)

    def get(self):
        try:
            return self.persistant_store[self.identifier]
        except KeyError as ke:
            self.set(self.initial_value)