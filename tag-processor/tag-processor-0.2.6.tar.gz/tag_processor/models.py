from builtins import object
from tag_processor.services import execute_tag_chain

__all__ = [
    'DataContainer',
    'FunctionTag',
    'ObjectTag',
    'DisjunctionTag',
    'TernaryTag',
    'ConstantTag'
]


class DataContainer(object):

    @staticmethod
    def dateformat(value, date_format):
        if not value:
            return None
        return value.strftime(date_format)

    @staticmethod
    def first(value, params):
        return value[0]

    @staticmethod
    def str(value, *args, **kwargs):
        return str(value)

    @staticmethod
    def round(value, prec):
        return round(value, int(prec)) if value else None


class DjangoDataContainer(DataContainer):

    @staticmethod
    def first(queryset, *args, **kwargs):
        if queryset is None:
            return queryset
        all = queryset.all()
        if all.exists():
            return all[0]
        return None

    @staticmethod
    def count(queryset, *args, **kwargs):
        if queryset is None:
            return 0
        return queryset.count()

    @staticmethod
    def concat(queryset, field, *args, **kwargs):
        if queryset is None:
            return queryset
        values = set()
        for item in queryset.all():
            value = DjangoDataContainer._get_field_value(item, field, None)
            if value:
                values.add(str(value))
        return ",".join(values)

    @staticmethod
    def min(queryset, field, *args, **kwargs):
        if queryset is None:
            return queryset

        values = DjangoDataContainer._get_values(queryset, field)
        if not values:
            return None
        return min(values)

    @staticmethod
    def max(queryset, field, *args, **kwargs):
        if queryset is None:
            return queryset
        values = DjangoDataContainer._get_values(queryset, field)
        if not values:
            return None
        return max(values)

    @staticmethod
    def sum(queryset, field, *args, **kwargs):
        if queryset is None:
            return queryset
        values = DjangoDataContainer._get_values(queryset, field)
        return sum(values)

    @staticmethod
    def _get_values(queryset, field):
        values = set()
        for item in queryset.all():
            value = DjangoDataContainer._get_field_value(item, field, None)
            if value:
                values.add(value)
        return values

    @staticmethod
    def _get_field_value(instance, field, default_value=None):
        field_path = field.split('__')
        attr = instance
        for elem in field_path:
            try:
                if isinstance(attr, list):
                    attr = attr[0]
                attr = getattr(attr, elem, None) or attr[elem]
            except AttributeError:
                return default_value
            except Exception:
                return default_value
        return attr


class FunctionTag(object):

    def __init__(self, value, params):
        self.value = value
        self.params = params

    def execute(self, data):
        if not self.value or not hasattr(self.value, '__call__'):
            return data

        return self.value(data, self.params)


class ObjectTag(object):

    def __init__(self, value):
        self.value = value

    def execute(self, data):
        if not data:
            return None
        result = getattr(data, self.value, None)
        if not result and callable(getattr(data, 'get', None)):
            result = data.get(self.value, None)
        return result


class DisjunctionTag(object):

    def __init__(self, elements):
        self.elements = elements

    def execute(self, data):
        if not data:
            return None
        for element in self.elements:
            result = element.execute(data)
            if result:
                return result
        return None


class TernaryTag(object):

    def __init__(self, condition, if_true, if_false):
        self.if_true = if_true
        self.if_false = if_false
        self.condition = condition

    def execute(self, data):
        if not data:
            return None
        if execute_tag_chain(self.condition, data):
            return self.if_true.execute()
            # return execute_tag_chain(self.if_true, data)
        else:
            return self.if_false.execute()
            # return execute_tag_chain(self.if_false, data)


class ConstantTag(object):

    def __init__(self, value):
        self.value = value

    def execute(self, *args, **kwargs):
        return self.value

