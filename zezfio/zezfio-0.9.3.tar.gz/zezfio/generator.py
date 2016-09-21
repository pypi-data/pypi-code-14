#  o  _  _  ._  
#  | _> (_) | | 
# _|           
#
import json
def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key,
                     ignore_dicts=True): _byteify(value,
                                                  ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle,
                  object_hook=_byteify),
        ignore_dicts=True)

def load_json(path):
    with open(path) as data_file:
        data = json_load_byteified(data_file)
    return data

#                                 
# _|_  _  ._ _  ._  |  _. _|_  _  
#  |_ (/_ | | | |_) | (_|  |_ (/_ 
#               |                 

import os
file_dir = os.path.dirname(__file__)
template_dir_rel = os.path.join(file_dir,"template")
template_dir = os.path.abspath(template_dir_rel)

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(template_dir))


def generate_server(json_path,db_path,debug=False):

    json_config = load_json(json_path)
    template = env.get_template('management.jinja2.py').render(json_config=json_config,
                                                               db_path=db_path)
    if debug:
        print template

    return template

def generate_fortran(json_path,debug=False):

    from zezfio.babel import c2stuff
    json_config = load_json(json_path)
    template = env.get_template('lib_fortran.jinja2.f90').render(json_config=json_config,
                                                                 c2stuff=c2stuff)
    if debug:
        print template

    return template

def importCode(code,name):

    import sys,imp

    module = imp.new_module(name)
    compiled_code = compile(code, '<string>', 'exec')
    exec compiled_code in module.__dict__
    sys.modules["module"] = module

    return module

def get_dict_module_server(json_path,db_path,debug=False):

    code = generate_server(json_path,db_path,debug)
    m = importCode(code, "zezfio_server")
    return m.d_instance
