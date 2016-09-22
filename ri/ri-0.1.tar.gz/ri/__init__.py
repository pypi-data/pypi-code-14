import os
import imp
import requests

def remote_import(uri, name=None):
    if not name:
        name = os.path.basename(uri).lower().rstrip('.py')

    r = requests.get(uri)
    r.raise_for_status()

    codeobj = compile(r.content, uri, 'exec')
    module = imp.new_module(name)
    exec (codeobj, module.__dict__)
    return module

