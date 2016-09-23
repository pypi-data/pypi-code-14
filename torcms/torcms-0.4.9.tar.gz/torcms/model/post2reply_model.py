# -*- coding:utf-8 -*-


import time

from torcms.core import tools
from torcms.model.core_tab import CabReply, CabPost2Reply


class MPost2Reply():
    def __init__(self):
        self.tab = CabPost2Reply
        try:
            CabPost2Reply.create_table()
        except:
            pass

    def insert_data(self, id_post, id_reply):
        uid = tools.get_uuid()
        try:
            self.tab.create(
                uid=uid,
                post_id=id_post,
                reply_id=id_reply,
                timestamp=time.time(),
            )
            return (uid)
        except:
            return False

    def get_by_id(self, in_uid):
        recs = self.tab.select().join(CabReply).where(self.tab.post_id == in_uid).order_by(self.tab.timestamp.desc())
        return recs
