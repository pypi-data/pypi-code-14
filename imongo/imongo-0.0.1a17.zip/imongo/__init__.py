# 项目：MongoDB数据库
# 作者：huangtao
# 邮件：hunto@163.com
# 创建：2015-09-13
# 修订：2016-08-29 拆分到imongo，成为独立的包

import sys
import mongoengine
import imongo.fixengine
from orange import *
from orange.config import Config
from .document import *

def mongo_init(is_flask=False,is_dev=None,db=None):
    if is_dev is None:
        is_dev=not('wsgi' in sys.argv[0] or is_installed(sys.argv[0])\
                   ) or 'test' in sys.argv[0]
    _config=Config(project='mongo',is_dev=is_dev)
    _config.load_config()
    config=_config.get('database') or {}
    config.setdefault('host','mongodb://localhost/mongo')
    config.setdefault('tz_aware',True)
    config.setdefault('connect',False)
    if _config.is_dev :
        config['host']='mongodb://localhost/test'
    mongoengine.connect('',**config)    

mongo_init()
