import json


def dj_serializer(queryset, result_key='result'):
    error = {"error": queryset}
    if queryset != str:
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
        json_data = json.dumps(dict_results)
        return json.loads(json_data)
    else:
        return json.loads(error)
