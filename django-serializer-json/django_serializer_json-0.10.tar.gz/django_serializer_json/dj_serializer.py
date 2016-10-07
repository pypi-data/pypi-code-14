import json


def json_loads(dict_results):
    json_data = json.dumps(dict_results)
    return json.loads(json_data)


def dj_serializer(queryset, result_key='result'):
    if not(isinstance(queryset, str) or isinstance(queryset, int)):
        dict_results = {}
        result_list = []
        for instance in queryset:
            loop_dict = {}
            for field in instance._meta.local_fields:
                field_name = field.name
                attribute = getattr(instance, field_name)
                loop_dict[field_name] = str(attribute)
            result_list.append(loop_dict)
        dict_results[result_key] = result_list
        return json_loads(dict_results)
    else:
        return json_loads({result_key: queryset})
