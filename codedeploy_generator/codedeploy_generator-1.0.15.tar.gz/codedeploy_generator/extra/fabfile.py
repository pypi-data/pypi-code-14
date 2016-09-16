import os, glob

import json

from jinja2 import Environment
import logging
from fabric.api import *

def render_file(config):
    if not os.path.exists('./dist/deployment/'):
        os.makedirs('./dist/deployment/')
    for path, subdirs, files in os.walk("./src/"):
        for name in files:
            in_file = open(os.path.join(path, name), "r")
            text = in_file.read()
            in_file.close()
            logging.warning('Processing %s', name)
            if "appspec" in name:
                out_file = open(os.path.join('./dist/', name), "w")
                out_file.write(Environment().from_string(text).render(config))
                out_file.close()
            else:
                out_file = open(os.path.join('./dist/deployment/', name), "w")
                out_file.write(Environment().from_string(text).render(config))
                out_file.close()

def restart():
    pass

@task
def dist():
    config = json.loads(open('package.json').read())
    render_file(config)

@task
def zip():
    local("cd ./dist; zip -r ../deployment-scripts.zip *")

@task
def serve():
    dist()
    zip()