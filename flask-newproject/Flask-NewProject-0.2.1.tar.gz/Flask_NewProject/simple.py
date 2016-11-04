from skeleton import SkeletonStructure
from script_info import app_simple, basic_test_for_flask
from sys import argv
import os


def simple():
    simple = SimpleStructure(argv[1])
    simple.add_content_to_app()

class SimpleStructure(object):

    def __init__(self, projectName):
        self.projectName = projectName


    def add_content_to_app(self):
        s = SkeletonStructure(self.projectName)
        s.create_directories_and_file()

        pwd = os.getcwd()

        with open(pwd+'/'+self.projectName+'/'+self.projectName+'/app.py', 'w') as app_file:
            app_file.write(app_simple())

        with open(pwd+'/'+self.projectName+'/tests/tests.py', 'w') as test_info:
            test_info.write(basic_test_for_flask())

        

        
