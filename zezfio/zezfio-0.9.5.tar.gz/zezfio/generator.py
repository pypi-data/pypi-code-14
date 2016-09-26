#  o  _  _  ._  
#  | _> (_) | | 
# _|           
#
import json
def load_json(path):
    with open(path) as f:
        data = json.load(f)
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
