class JsonRequestDeserializer(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, dict):
                setattr(self, a, JsonRequestDeserializer(b))
            elif isinstance(b, list):
                items = [self._create_obj_by_type(item) for item in b]
                setattr(self, a, items)
            else:
                setattr(self, a, self._create_obj_by_type(b))

    @staticmethod
    def _create_obj_by_type(obj):
        obj_type = type(obj)
        if obj_type == dict:
            return JsonRequestDeserializer(obj)
        if obj_type == list:
            return [JsonRequestDeserializer._create_obj_by_type(item) for item in obj]
        if JsonRequestDeserializer._is_primitive(obj):
            return obj_type(obj)
        return obj

    @staticmethod
    def _is_primitive(thing):
        primitive = (int, str, bool, float, unicode)
        return isinstance(thing, primitive)
