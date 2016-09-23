# -*- coding:utf-8 -*-

import time
from torcms.model.core_tab import CabPic
from torcms.model.supertable_model import MSuperTable

class MEntity(MSuperTable):
    def __init__(self):
        self.tab = CabPic
        try:
            CabPic.create_table()
        except:
            pass

    def getall(self):
        return CabPic.select()

    def get_id_by_impath(self, imgpath):
        uu = CabPic.select().where(CabPic.imgpath == imgpath)
        if uu.count() == 1:
            return uu.get().uid
        elif uu.count() > 1:
            return False
        else:
            return False

    def insert_data(self, signature, impath):
        entry = CabPic.create(
            uid=signature,
            imgpath=impath,
            create_timestamp=time.time()
        )
        return entry
