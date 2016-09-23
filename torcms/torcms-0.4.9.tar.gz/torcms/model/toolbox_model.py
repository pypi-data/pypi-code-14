# -*- coding:utf-8 -*-

from torcms.core import tools
from torcms.model.core_tab import TabToolbox


class MToolbox(object):
    def __init__(self):
        try:
                TabToolbox.create_table()
        except:
            pass

    def query_recent(self, user_id, num = 10):
        return TabToolbox.select().where(TabToolbox.user == user_id).order_by(TabToolbox.order).limit(num)

    def query_most(self, num):
        return TabToolbox.select().limit(num)

    def get_by_signature(self, user_id, app_id):
        try:
            return TabToolbox.get((TabToolbox.user==user_id) & (TabToolbox.app== app_id))
        except:
            return False

    def add_or_update(self, user_id, app_id,title,  order ):

        if self.get_by_signature(user_id, app_id):
            tt = self.get_by_signature(user_id, app_id)
            entry = TabToolbox.update(
                order=order,
            ).where(TabToolbox.uid == tt.uid)
            entry.execute()

        else:
            entry = TabToolbox.create(
                uid = tools.get_uuid(),
                user = user_id,
                cnt = title,
                title = title,
                app  = app_id,
                order = order,
            )

