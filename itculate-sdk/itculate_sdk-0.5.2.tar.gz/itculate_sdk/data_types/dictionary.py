from collections import defaultdict

from itculate_sdk.data_types.types import TypedValue


class Dictionary(object):
    D_TYPE_VERTEX = "vertex"
    D_TYPE_TIMESERIES = "timeseries"

    # Maintain a static version of the dictionary (so we don't keep on sending updates)
    dictionary = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    dictionary_changed = False

    @classmethod
    def reset_dictionary(cls):
        cls.dictionary = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        cls.dictionary_changed = False

    @classmethod
    def update_and_strip(cls, d_type, vertex_type, attribute, value):
        """
        Updates the dictionary repository with new meta data, then return a simple value (instead of TypedValue object)

        :param str d_type: Dictionary item type. Either "vertex" or "timeseries"
        :param str vertex_type: Vertex Type
        :param str attribute: Name of attribute
        :param value: Value of attribute (if TypedValue, this will be used to extract meta-data)

        :return: The plain value (stripped off TypedValue)
        """
        if isinstance(value, TypedValue):
            meta_data = value.meta_data
            current_value = cls.dictionary[d_type][vertex_type][attribute]

            if current_value != meta_data:
                current_value.update(meta_data)
                cls.dictionary_changed = True

            return value.value

        else:
            return value
