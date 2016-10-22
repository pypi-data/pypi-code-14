# -*- coding:utf-8 -*-

import datetime

import tornado.escape

from torcms.core import tools
from .core_tab import CabWiki
from .supertable_model import MSuperTable


class MWiki(MSuperTable):
    def __init__(self):
        self.tab = CabWiki

    def query_all(self, limit_num = 50, by_uid = 'False'):
        if by_uid:
            return self.tab.select().order_by(self.tab.uid).limit(limit_num)
        else:
            return self.tab.select().limit(limit_num)

    def update(self, uid, post_data):
        title = post_data['title'][0].strip()
        if len(title) < 2:
            return False

        cnt_html = tools.markdown2html(post_data['cnt_md'][0])

        entry = CabWiki.update(
            title=title,
            date=datetime.datetime.now(),
            cnt_html=cnt_html,
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=tools.timestamp(),
        ).where(CabWiki.uid == uid)
        entry.execute()

    def insert_data(self, post_data):
        title = post_data['title'][0].strip()
        if len(title) < 2:
            return False

        uu = self.get_by_wiki(title)
        if uu :
            return (False)

        cnt_html = tools.markdown2html(post_data['cnt_md'][0])

        entry = CabWiki.create(
            title=title,
            date=datetime.datetime.now(),
            cnt_html=cnt_html,
            uid=tools.get_uu8d(),
            time_create=tools.timestamp(),
            user_name=post_data['user_name'],
            cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
            time_update=tools.timestamp(),
            view_count=1,
        )
        return (entry.uid)

    def query_dated(self, num=10):
        return CabWiki.select().order_by(CabWiki.time_update.desc()).limit(num)

    def query_most(self, num=8):
        return CabWiki.select().order_by(CabWiki.view_count.desc()).limit(num)

    def update_view_count(self, citiao):
        entry = CabWiki.update(view_count=CabWiki.view_count + 1).where(CabWiki.title == citiao)
        entry.execute()

    def update_view_count_by_uid(self, uid):
        entry = CabWiki.update(view_count=CabWiki.view_count + 1).where(CabWiki.uid == uid)
        entry.execute()

    def get_by_wiki(self, citiao):
        q_res = CabWiki.select().where(CabWiki.title == citiao)
        tt = q_res.count()
        if tt == 0 or tt > 1:
            return None
        else:
            self.update_view_count(citiao)
            return q_res.get()

    def get_by_title(self, in_title):
        # Aka get_by_wiki
        return self.get_by_wiki(in_title)
