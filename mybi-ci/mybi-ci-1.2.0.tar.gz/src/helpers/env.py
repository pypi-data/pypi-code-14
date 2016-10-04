__author__ = 'marcoantonioalberoalbero'

import configparser
import os


def read_config():
    global config, sections
    try:
        init = os.environ['MYBICI_SETUP_FILE']
        sections = os.environ['MYBICI_SETUP_FILE_SECTIONS'].split(',')
        config = configparser.ConfigParser()
        config.read(init)
    except:
        raise Exception("Need to define MYBICI_SETUP_FILE and "
                        "MYBICI_SETUP_FILE_SECTIONS environment "
                        "variables (https://github.com/periket2000/mybi-ci)")
    return config
