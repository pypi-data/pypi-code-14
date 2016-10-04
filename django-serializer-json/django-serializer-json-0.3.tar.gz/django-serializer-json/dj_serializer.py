import json


def dj_serializer(queryset):
    dict_res = {}
    res = []
    for instance in queryset:
        d = {}
        for field in instance._meta.local_fields:
            g = field.name
            x = getattr(instance, g)
            d[g] = str(x)
        res.append(d)

    dict_res['result'] = res
    json_data = json.dumps(dict_res)
    return json_data
