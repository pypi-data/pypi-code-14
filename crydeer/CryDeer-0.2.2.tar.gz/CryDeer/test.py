#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import json

jsonPath = "company.json"
jsonFile = open(jsonPath, "r")
com_names = json.loads(jsonFile.read())
jsonFile.close()
print(com_names["bht"])
