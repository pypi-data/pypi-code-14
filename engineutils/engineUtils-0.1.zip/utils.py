#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import time

def generate_sid(apply_id):
    now = datetime.datetime.now()
    starttime = int((now).strftime("%s"))
    sid = "%d%d" % (apply_id, starttime)
    return sid

def sid():
    sid = int( time.time() *100)
    return sid

#为对象加上object_type和object_id
def append_object_type_and_id(obj, obj_type, object_id):
    if type(obj) is not dict:
        return

    obj[u'object_type'] = obj_type  ## 对象类型
    obj[u'object_id'] = object_id  ## 对象id
    return

#为CBM 添加新对象 object_type和object_id
def append_new_object_to_cbm(cbm, obj, obj_type, object_id):
    if type(cbm) is not dict or type(obj) is not dict:
        print u"invalid cbm or new object."
        return

    obj[u'object_type'] = obj_type  ## 对象类型
    obj[u'object_id'] = object_id  ## 对象id

    obj_key = obj_type + u"_" + unicode(object_id)
    cbm[obj_key] = obj
    return