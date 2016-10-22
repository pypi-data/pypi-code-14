# -*- coding:utf-8 -*-


from torcms.core import tools
from torcms.model.core_tab import g_WikiHist
from torcms.model.supertable_model import MSuperTable


class MPageHist(MSuperTable):
    def __init__(self):
        self.tab = g_WikiHist
        try:
            g_WikiHist.create_table()
        except:
            pass

    def insert_data(self, raw_data):
        uid = tools.get_uuid()

        g_WikiHist.create(
                uid=uid,
                title=raw_data.title,
                # date=raw_data.date,
                wiki_id=raw_data.uid,
                # time_create=raw_data.time_create,
                user_name=raw_data.user_name,
                cnt_md=raw_data.cnt_md,
                time_update=raw_data.time_update,

            )
        return True
