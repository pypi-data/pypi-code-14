#!/usr/bin/env python

"""Used to create a new Flask project with some data already pre-created when starting a new project."""


# This is called to create a new Flask project taking an argument of project name
# This will create a simple as follows:
#
# in terminal run
# $ FlaskProject FlaskApp
#
# will create the structure:
# 
# FlaskApp/
# |
# --FlaskApp/
#   |
#   --app.py
#   |
#   tests/
#     |
#     --test_flask.py

# So this will make a direstory and subdirectory based on user input,
# the create a directory call tests, then create two files called
# app.py, as the main program to run, and test_flask.py in the tests
# directory to write your flask tests.

import os
from sys import argv


def skeleton():
    # will create a skeleton project with blank files.
    create_new_project()

def create_dirs(path):
    directory = os.path.dirname(path)
    if not os.path.exists(path):
        os.mkdir(path)
        
def create_new_project():
    pwd = os.getcwd()
    # 1) create directories bases on argv[1]
    PROJECT_DIR = pwd+'/'+argv[1]
    PROJECT_PACKAGE_DIR = PROJECT_DIR+'/'+argv[1]
    TESTS_IN_PACKAGE = PROJECT_PACKAGE_DIR+'/tests'
    
    create_dirs(PROJECT_DIR)
    create_dirs(PROJECT_PACKAGE_DIR)
    create_dirs(TESTS_IN_PACKAGE)

    # 2) crete files app.py and tests.py    
    open(PROJECT_PACKAGE_DIR+'/app.py', 'a').close()
    open(TESTS_IN_PACKAGE+'/tests.py', 'a').close()
    


#if __name__ == "__main__":
#    create_new_project()
