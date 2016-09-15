# -*- coding: utf-8 -*-

class Test:
    pass


t = Test()
print str(t.__class__).split('.')[-1]