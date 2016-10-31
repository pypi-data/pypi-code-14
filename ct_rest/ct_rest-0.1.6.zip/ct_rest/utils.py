# -*- coding:utf-8 -*-
import datetime, time, django, copy


def to_dict(target, spread = None):
    '''
    turn models object to dict
    Args:
        target:

    Returns:

    '''
    def _to_dict(modelIns, spread):
        temp = copy.deepcopy(modelIns.__dict__)
        for k,v in temp.items():
            if k[0] == "_":
                del temp[k]
            elif type(v) == datetime.datetime:
                temp[k] = time.mktime(datetime.datetime.timetuple(v))
        if spread:
            if type(spread) == str:
                spread = [spread]
            for s in spread:
                temp[s] = getattr(modelIns,s)
        return temp

    if type(target) == django.db.models.query.QuerySet:
        resp = []
        for ins in target:
            resp.append(_to_dict(ins, spread))
        return resp
    else:
        return _to_dict(target, spread)