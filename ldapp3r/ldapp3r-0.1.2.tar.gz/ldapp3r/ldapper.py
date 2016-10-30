from ldap3 import MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE, MODIFY_INCREMENT
class LdapperException(Exception):
    def __init__(self, message):
        self.message = message

class LdapperInterface(object):
    @staticmethod
    def define(searchBase, primarySearch, **kwargs):
        return LdapperModelDefinition(searchBase, primarySearch, **kwargs)


class LdapperModelDefinition(object):
    def __init__(self, searchBase, primarySearch, attributes=['*'], connection=None, wrapper=True):
        self._wrapper = wrapper
        self._searchBase = searchBase
        if "(" not in primarySearch:
            primarySearch = "(%s)" % primarySearch
        self._primarySearch = primarySearch
        self._attributes = attributes
        self._connection = connection

    def using(self, connection):
        return LdapperModelDefinition(self._searchBase,
                self._primarySearch,
                attributes=self._attributes,
                wrapper=self._wrapper,
                connection=connection)

    def get(self, primary):
        if not self._connection:
            raise LdapperException("No connection for ModelDefinition, consider chaining with using()")
        if not self._connection.search(self._searchBase, self._primarySearch % primary, attributes=self._attributes):
            raise LdapperException(self._connection.result)
        if len(self._connection.entries) != 1:
            return None
        else:
            if self._wrapper:
                return LdapperModelWrapper(self._connection.entries[0])
            else:
                return self._connection.entries[0]

    def find(self, **kwargs):
        search = "(&"
        for pair in kwargs.items():
            search += "(%s=%s)" % pair
        search += ")"
        return self.find_raw(search)

    def find_raw(self, search):
        if not self._connection:
            raise LdapperException("No connection for ModelDefinition, consider chaining with using()")
        if not self._connection.search(self._searchBase, search, attributes=self._attributes):
            raise LdapperException(self._connection.result)
        if self._wrapper:
            return [LdapperModelWrapper(e) for e in self._connection.entries]
        else:
            return self._connection.entries

    def save(self, obj):
        if not self._connection:
            raise LdapperException("No connection for ModelDefinition, consider chaining with using()")
        # empty entry assumes new object
        if obj._entry == None:
            pass
        else:
            changes = {}
            for key, value in obj._newValues.items():
                if value == None: # delete
                    changes[key] = [(MODIFY_DELETE,[])]
                elif not hasattr(obj._entry, key):
                    if isinstance(value, list):
                        changes[key] = [(MODIFY_ADD,value)]
                    else:
                        changes[key] = [(MODIFY_ADD, [value])]
                else:
                    if isinstance(value, list):
                        changes[key] = [(MODIFY_REPLACE,value)]
                    else:
                        changes[key] = [(MODIFY_REPLACE, [value])]
            if not self._connection.modify(obj._entry.entry_dn, changes):
                raise LdapperException(self._connection.result)


class LdapperModelWrapper:
    def __init__(self, entry):
        self._entry = entry
        self._newValues = {}

    def __getattr__(self, key):
        if key in self._newValues:
            return self._newValues[key]
        else:
            return getattr(self._entry, key).value

    def __setattr__(self, key, value):
        if not key.startswith('_'):
            self._newValues[key] = value
        else:
            self.__dict__[key] = value
