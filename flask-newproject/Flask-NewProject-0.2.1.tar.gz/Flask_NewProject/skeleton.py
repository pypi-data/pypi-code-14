# This is to create a skeleton structure of a flask web app with no extra content
import os
from sys import argv
from CreateDirs import create_dirs


def skeleton():
    skeleton = SkeletonStructure(argv[1])
    skeleton.create_directories_and_file()


class SkeletonStructure(object):

    def __init__(self, projectName):
        self.projectName = projectName

        self.pwd = os.getcwd()
        self.project_folders = ['/bin', '/docs', '/tests']
        self.package_folders = ['/static', '/templates']

    def create_directories_and_file(self):
        # This will create the main project folder, package folder(same name)
        # docs folder and tests folder
        _PROJECT_FOLDER = self.pwd + '/' + self.projectName
        create_dirs(_PROJECT_FOLDER)
        for folder in self.project_folders:
            create_dirs(_PROJECT_FOLDER + folder)
        
        _PACKAGE_FOLDER = _PROJECT_FOLDER + '/' + self.projectName
        create_dirs(_PACKAGE_FOLDER)

        open(_PACKAGE_FOLDER + '/app.py', 'a').close()
        open(_PACKAGE_FOLDER + '/__init__.py', 'a').close()

    
        
