#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import json

dic = {}
file = open("test", "r")
first = True
key = ""
for line in file.readlines():
    if first:
        key =  line[:-1]
        first = False
    else:
        value = line[:-1]
        dic[key] = value
        first = True
file.close()
jsonFile = open("test", "w")
jsonFile.write(json.dumps(dic,ensure_ascii=False))
jsonFile.close()
