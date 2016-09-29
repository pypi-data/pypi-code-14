import irpy
import json
import os
def importCode(code,name):

    import sys,imp

    module = imp.new_module(name)
    compiled_code = compile(code, '<string>', 'exec')
    exec compiled_code in module.__dict__
    sys.modules["module"] = module

    return module

def check_list(l,mode="folder"):

    if mode == "folder":
        fct = os.path.isdir
    elif mode == "file":
        fct = os.path.isfile

    l_error = [i for i in l if not fct(i)]
    if l_error:
        raise KeyError("{0} need to be a {1}".format(l_error,mode))


class Generator(object):

    @irpy.lazy_property_leaves(mutables=["db_path","list_folder_user","list_file_user"])
    def __init__(self,arguments):

        db_path_rel = arguments["<ezfio_folder>"]
        self.db_path = os.path.abspath(db_path_rel)

        try:
            l = arguments["--dir"]
            check_list(l,mode="folder")
        except KeyError:
            self.list_folder_user = []
        else: 
            self.list_folder_user = l

        try:
            l = arguments["--file"]
            check_list(l,mode="file")
        except KeyError:
            self.list_file_user = []
        else: 
            self.list_file_user = l

    @irpy.lazy_property
    def list_file(self):
        
        l = self.list_file_user
        for folder in self.list_folder_user:
            l += [os.path.join(folder,i) for i in os.listdir(folder)]
        
        if not l:
            raise KeyError("Provide ether list_file_user or list_folder_user")
        else:
            check_list(l,mode="file")
        return l

    @irpy.lazy_property
    def json_config(self):
        data = dict()

        for path in self.list_file:
            with open(path) as f:
                data.update(json.load(f))

        return data

    @irpy.lazy_property
    def jinja_env(self):
        file_dir = os.path.dirname(__file__)
        template_dir_rel = os.path.join(file_dir,"template")
        template_dir = os.path.abspath(template_dir_rel)
        
        from jinja2 import Environment, FileSystemLoader
        return Environment(loader=FileSystemLoader(template_dir))

    @irpy.lazy_property
    def template_server(self):
        if not self.db_path:
            raise KeyError("You need to set the db_path to generate the server")

        template = self.jinja_env.get_template('management.jinja2.py').render(json_config=self.json_config,
                                                                       db_path=self.db_path)
        return template

    @irpy.lazy_property
    def template_fortran(self):

        from zezfio.babel import c2stuff
        template = self.jinja_env.get_template('management.jinja2.py').render(json_config=self.json_config,
                                                                       c2stuff=c2stuff)
        return template

    @irpy.lazy_property
    def d_instance(self):
        m = importCode(self.template_server, "zezfio_server")
        return m.d_instance





