#!/usr/bin/env python

FootmarkDir = '/etc/footmark/'
FootmarkConfig = FootmarkDir + 'logging.conf'

FootmarkLogsDir = '/var/log/footmark/'

logging_config = '''
[loggers]
keys=root

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=form01

[logger_root]
level=NOTSET
handlers=consoleHandler,fileHandler

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=form01
args=()

[handler_fileHandler]
class=handlers.TimedRotatingFileHandler
level=DEBUG
formatter=form01
args=('footmark.log','D',1,7)

[formatter_form01]
format=%(asctime)s [%(levelname)s] %(filename)s %(funcName)s %(lineno)d: %(message)s
'''
def make_dir():
    if not os.path.exists(FootmarkDir):
        os.makedirs(FootmarkDir)
    if not os.path.exists(FootmarkLogsDir):
        os.makedirs(FootmarkLogsDir)

def add_config():
    file_pb = open(FootmarkConfig, 'wb')
    file_pb.write(logging_config)
    file_pb.close()

if __name__ == "__main__":
    try:
        import os
    except:
        pass
    make_dir()
    add_config()