# -*- coding:utf-8 -*-

import config
from torcms.core import tools
from torcms.model.core_tab import g_Tag as CabLabel
from torcms.model.core_tab import g_Post
from torcms.model.core_tab import g_Post2Tag as CabPost2Label
from torcms.model.supertable_model import MSuperTable


class MLabel(MSuperTable):
    def __init__(self):
        self.tab = CabLabel


    def get_id_by_name(self, tag_name, kind = '11'):
        uu = self.tab.select().where((self.tab.name == tag_name) & (self.tab.kind ==  kind))
        if uu.count() == 1:
            return uu.get().uid
        elif uu.count() > 1:
            for x in uu:
                self.delete(x.uid)
        else:
            return self.create_tag(tag_name, kind)

    def create_tag(self, tag_name, kind='11'):

        cur_count = self.tab.select().where((self.tab.name == tag_name) & (self.tab.kind ==  kind)).count()
        if cur_count > 0:
            return False

        uid = tools.get_uu4d_v2()
        while self.tab.select().where(self.tab.uid == uid).count() > 0:
            uid = tools.get_uu4d_v2()

        self.tab.create(
            uid=uid,
            slug = uid,
            name=tag_name,
            order = 1,
            count=0,
            kind = kind,
        )
        return uid


class MPost2Label(MSuperTable):
    def __init__(self):
        self.tab = CabPost2Label
        self.tab_label = CabLabel
        self.tab_post = g_Post
        self.mtag = MLabel()
        try:
            CabPost2Label.create_table()
        except:
            pass
    def remove_relation(self, post_id, tag_id):
        entry = self.tab.delete().where((self.tab.post == post_id) & (self.tab.tag == tag_id))
        entry.execute()

    def generate_catalog_list(self, signature):
        tag_infos = self.get_by_id(signature)
        out_str = ''
        for tag_info in tag_infos:
            tmp_str = '<li><a href="/tag/{0}" >{1}</a></li>'.format(tag_info.tag, tag_info.catalog_name)
            out_str += tmp_str
        return out_str

    def get_by_id(self, idd, kind = '11'):
        print('select kind: {0}'.format(kind))
        return self.tab.select().join(self.tab_label).where((self.tab.post == idd) & (self.tab_label.kind == kind) )



    def get_by_info(self, post_id, catalog_id, kind =  '11'):
        tmp_recs = self.tab.select().join(self.tab_label).where((self.tab.post == post_id) & (self.tab.tag == catalog_id) & (self.tab_label.kind == kind))

        if tmp_recs.count() > 1:
            ''' 如果多于1个，则全部删除
            '''
            for tmp_rec in tmp_recs:
                self.delete(tmp_rec.uid)
            return False

        elif tmp_recs.count() == 1:
            return tmp_recs.get()
        else:
            return False

    def add_record(self, post_id, tag_name, order=1, kind = '11'):
        print('Add label kind: {0}'.format(kind))
        tag_id = self.mtag.get_id_by_name(tag_name, kind)
        tt = self.get_by_info(post_id, tag_id, kind=kind)
        if tt:
            entry = self.tab.update(
                order=order,
            ).where(self.tab.uid == tt.uid)
            entry.execute()
        else:
            entry = self.tab.create(
                uid=tools.get_uuid(),
                post=post_id,
                tag=tag_id,
                order=order,
                kind = kind,
            )
            return entry.uid


    def total_number(self, slug):
        return self.tab_post.select().join(self.tab).where(self.tab.tag == slug).count()

    def query_pager_by_slug(self, slug, current_page_num=1):
        return self.tab_post.select().join(self.tab).where(self.tab.tag == slug).paginate(current_page_num,
                                                                                          config.page_num)
