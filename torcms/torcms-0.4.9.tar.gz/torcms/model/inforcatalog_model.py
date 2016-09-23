# -*- coding:utf-8 -*-

from torcms.model.core_tab import TabCatalog
from torcms.model.postcatalog_model import MPostCatalog

class MInforCatalog(MPostCatalog):
    def __init__(self):
        self.tab = TabCatalog
        try:
            TabCatalog.create_table()
        except:
            pass

