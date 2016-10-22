# -*- coding: utf-8

import sys

from torcms.model.category_model import MCategory

from torcms.model.infor2catalog_model import MInfor2Catalog
from torcms.core.tools import constant
def run_update_count():
    mapp2cat = MInfor2Catalog()
    mappcat = MCategory()
    for rec in mappcat.query_all( kind = constant['cate_info'] ):
        uid= rec.uid
        print(rec.name)
        # uuvv = mapp.query_extinfo_by_cat(uid)
        uuvv = mapp2cat.query_by_catid(rec.uid)
        print(uid, uuvv.count())
        mappcat.update_count(uid, uuvv.count())
