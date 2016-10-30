# -*- coding: utf-8 -*-
import json


class BufferedJSON:
    def __init__(self):
        pass

    def load(self, fileName):
        openCount = 0
        closeCount = 0
        entity = ""
        with open(fileName, 'r') as file:
            for line in file:
                if openCount == 0 and '[' in line:
                    continue
                if '{' in line:
                    openCount += 1
                    entity += line.replace('\n', '')
                elif '}' in line:
                    closeCount += 1
                    entity += line.replace('\n', '')
                else:
                    entity += line.replace('\n', '')

                if openCount == closeCount and openCount != 0: # entity is correct
                    if entity[-1] == ',':
                        entity = entity[:-1]
                    yield json.loads(entity)
                    entity = ""
                    openCount = 0
                    closeCount = 0

