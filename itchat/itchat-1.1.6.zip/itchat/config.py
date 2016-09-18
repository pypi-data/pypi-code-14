import os, platform

from . import content # this is for creating pyc

DIR = os.getcwd()
BASE_URL = 'https://login.weixin.qq.com'
OS = platform.system() #Windows, Linux, Darwin

WELCOME_WORDS = 'Hello World!'
