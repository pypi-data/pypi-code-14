# -*- coding:utf-8 -*-


from torcms.model.core_tab import TabApp, TabCatalog, TabApp2Catalog
from torcms.model.post2catalog_model import MPost2Catalog


class MInfor2Catalog(MPost2Catalog):
    def __init__(self):
        self.tab_post2catalog = TabApp2Catalog
        self.tab_catalog = TabCatalog
        self.tab_post = TabApp
        try:
            TabApp2Catalog.create_table()
        except:
            pass
