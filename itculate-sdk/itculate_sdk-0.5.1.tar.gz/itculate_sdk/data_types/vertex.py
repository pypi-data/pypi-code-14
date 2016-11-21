from itculate_sdk.data_types.dictionary import Dictionary
from .utils import ReadOnlyDict, check_keys

_VERTEX_NAME_ATTR = "_name"
_VERTEX_TYPE_ATTR = "_type"
_VERTEX_KEYS_ATTR = "_keys"
_VERTEX_PRIMARY_KEY_ATTR = "_primary_key"


class Vertex(object):
    def __init__(self, vertex_type, name, keys, primary_key_id=None, data=None, **kwargs):
        """
        Defines a client-side vertex. This is basically a set of attributes (with special ones prefixed with '_').

        :param str vertex_type: Vertex type
        :param str primary_key_id: Name of key (within 'keys') designated as primary key (must be globally unique)
        :param dict keys: A set of unique keys identifying this vertex
        :param str name: Name for vertex
        :param dict data: Set of initial values to assign to vertex (optional)
        :param kwargs: Any additional key:value pairs that should be assigned to vertex.
        """
        assert vertex_type, "Type is mandatory"
        assert name, "Name is mandatory"

        check_keys(keys)
        assert primary_key_id, "primary_key_id is mandatory"
        assert primary_key_id in keys, "primary_key_id {} must point to a key in keys {}".format(primary_key_id, keys)

        if data is not None:
            assert isinstance(data, dict), "data must be of type dict"
            d = data

        else:
            d = {}

        # Add any keyword args to the dictionary
        if kwargs:
            d.update(kwargs)

        # Get the meta-data from each of the attributes
        for k, v in d.iteritems():
            stripped_value = Dictionary.update_and_strip(d_type=Dictionary.D_TYPE_VERTEX,
                                                         vertex_type=vertex_type,
                                                         attribute=k,
                                                         value=v)
            d[k] = stripped_value

        # Add the essentials (to make sure they override everything)
        d.update({
            _VERTEX_TYPE_ATTR: vertex_type,
            _VERTEX_KEYS_ATTR: ReadOnlyDict(keys),
            _VERTEX_NAME_ATTR: name,
            _VERTEX_PRIMARY_KEY_ATTR: primary_key_id,
        })

        # Finally - update self and set the dirty flag (False as this is the initial setting)
        self._d = d

    @property
    def type(self):
        return self._d[_VERTEX_TYPE_ATTR]

    @property
    def name(self):
        return self._d[_VERTEX_NAME_ATTR]

    @name.setter
    def name(self, name):
        self[_VERTEX_NAME_ATTR] = name

    @property
    def keys(self):
        """
        :rtype: dict
        :return The vertex keys (DO NOT CHANGE - use add_key instead!!!)
        """
        return ReadOnlyDict(self._d[_VERTEX_KEYS_ATTR])

    @property
    def primary_key(self):
        return self.keys[self.primary_key_id]

    @property
    def primary_key_id(self):
        return self._d[_VERTEX_PRIMARY_KEY_ATTR]

    @property
    def document(self):
        """
        Provides access to internal document representing this vertex

        :rtype: dict[str, str]
        """
        return ReadOnlyDict(self._d)

    def update(self, d):
        """
        Override the default set to handle dirty flag

        :param dict[str, str] d: Dict to update with
        """
        assert isinstance(d, dict), "Expecting dict"
        assert _VERTEX_KEYS_ATTR not in d, "Cannot update keys!"
        self._d.update(d)

    def __setitem__(self, key, value):
        """
        Override the default set to handle dirty flag
        """
        assert not key.startswith("_"), "Cannot modify a special/internal attribute"
        self._d.__setitem__(key, value)

    def __getitem__(self, item):
        return self._d.__getitem__(item)

    def __delitem__(self, key):
        assert not key.startswith("_"), "Cannot delete a special/internal attribute"
        return self._d.__delitem__(key)

    def __contains__(self, item):
        return self._d.__contains__(item)

    def get(self, key, default=None):
        return self._d.get(key, default)

    def __cmp__(self, other):
        assert isinstance(other, Vertex), "Only Vertex comparisons are supported"
        return cmp(self._d, other._d)

    def __str__(self):
        return "Vertex ({}) {}: {}".format(self.type, self.name, self.keys)
