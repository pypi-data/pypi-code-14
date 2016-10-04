# -*- coding:utf-8 -*-

from torcms.model.core_tab import  g_Rel, g_Post
from torcms.model.relation_model import MRelation


class MInforRel(MRelation):
    def __init__(self):
        self.tab_relation = g_Rel
        self.tab_post = g_Post
        try:
            g_Rel.create_table()
        except:
            pass


class MRelPost2Infor(MRelation):
    def __init__(self):
        MRelation.__init__(self)
        self.tab_relation = g_Rel
        self.tab_post = g_Post
        try:
            self.tab_relation.create_table()
        except:
            pass


class MRelInfor2Post(MRelation):
    def __init__(self):
        MRelation.__init__(self)
        self.tab_relation = g_Rel
        self.tab_post = g_Post
        try:
            self.tab_relation.create_table()
        except:
            pass
