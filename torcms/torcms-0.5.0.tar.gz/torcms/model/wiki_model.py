# -*- coding:utf-8 -*-

import datetime

import tornado.escape

from torcms.core import tools
from torcms.model.core_tab import g_Wiki
from torcms.model.supertable_model import MSuperTable


class MWiki(MSuperTable):
    def __init__(self):
        self.tab = g_Wiki
        try:
            self.tab.create_table()
        except:
            pass

    def update(self, uid, post_data):
        title = post_data['title'][0].strip()
        if len(title) < 2:
            return False

        cnt_html = tools.markdown2html(post_data['cnt_md'][0])

        entry = self.tab.update(
            title=title,
            date=datetime.datetime.now(),
            cnt_html=cnt_html,
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=tools.timestamp(),
            kind=post_data['kink'],
        ).where(self.tab.uid == uid)
        entry.execute()

    def insert_data(self, post_data):
        title = post_data['title'].strip()
        if len(title) < 2:
            return False

        uu = self.get_by_wiki(title)
        if uu:
            self.update(uu.uid, post_data)
            return

        cnt_html = tools.markdown2html(post_data['cnt_md'])

        entry = self.tab.create(
            # No page slug should startswith '_'
            uid=post_data['uid'] if 'uid' in post_data else '_' + tools.get_uu8d(),
            title=title,
            date=datetime.datetime.now(),
            cnt_html=cnt_html,
            time_create=post_data['time_create'] if 'time_craete' in post_data else tools.timestamp(),
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md']),
            time_update=tools.timestamp(),
            view_count=1,
            kind=post_data['kind'] if 'kind' in post_data else 1,
        )
        return (entry.uid)

    def query_dated(self, num=10, kind=1):
        return self.tab.select().where(self.tab.kind == kind).order_by(self.tab.time_update.desc()).limit(num)

    def query_most(self, num=8, kind=1):
        return self.tab.select().where(self.tab.kind == kind).order_by(self.tab.view_count.desc()).limit(num)

    def update_view_count(self, citiao):
        entry = self.tab.update(view_count=self.tab.view_count + 1).where(self.tab.title == citiao)
        entry.execute()

    def update_view_count_by_uid(self, uid):
        entry = self.tab.update(view_count=self.tab.view_count + 1).where(self.tab.uid == uid)
        entry.execute()

    def get_by_wiki(self, citiao):
        q_res = self.tab.select().where(self.tab.title == citiao)
        tt = q_res.count()
        if tt == 0 or tt > 1:
            return None
        else:
            self.update_view_count(citiao)
            return q_res.get()

    def get_by_title(self, in_title):
        # Aka get_by_wiki
        return self.get_by_wiki(in_title)
