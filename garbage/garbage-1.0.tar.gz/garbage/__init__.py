#!/bin/env python
import sys
import importlib
help("modules")

for n in sys.modules:
    try:
        mod = importlib.import_module(n)
        globals().update(mod.__dict__)
    except:
        pass
