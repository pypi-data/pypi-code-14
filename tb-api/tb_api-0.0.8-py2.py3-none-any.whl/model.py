from os.path import abspath


class Config(object):
    def __init__(self, project_dir, debug, port):
        self.debug = debug
        self.project_dir = abspath(project_dir)
        self.port = port
        self.loader = None
