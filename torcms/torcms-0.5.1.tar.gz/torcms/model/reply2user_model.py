# -*- coding:utf-8 -*-

import datetime
import time

import peewee
import tornado.escape
import config
from torcms.core import tools
from torcms.model.core_tab import g_Post2Tag
from torcms.model.core_tab import g_Voter2Reply
from torcms.model.core_tab import g_Reply

from torcms.model.core_tab import g_Post2Reply
from torcms.model.supertable_model import MSuperTable


class MReply2User(MSuperTable):
    def __init__(self):
        self.tab = g_Voter2Reply
        try:
            g_Voter2Reply.create_table()
        except:
            pass

    def update(self, uid, post_data, update_time=False):
        pass
        # cnt_html = tools.markdown2html(post_data['cnt_md'][0])
        #
        # entry = CabVoter2Reply.update(
        #     title=post_data['title'][0],
        #     date=datetime.datetime.now(),
        #     cnt_html=cnt_html,
        #     user_name=post_data['user_name'],
        #     cnt_md=tornado.escape.xhtml_escape(post_data['cnt_md'][0]),
        #     time_update=time.time(),
        #     logo=post_data['logo'][0],
        #     keywords=post_data['keywords'][0],
        #     src_type=post_data['src_type'][0] if ('src_type' in post_data) else 0
        # ).where(CabVoter2Reply.uid == uid)
        #
        # entry.execute()

    def insert_data(self, user_id, reply_id):

        record = g_Voter2Reply.select().where(
            (g_Voter2Reply.reply_id == reply_id) & (g_Voter2Reply.voter_id == user_id))

        if record.count() > 0:
            return (False)

        try:
            g_Voter2Reply.create(
                uid=tools.get_uuid(),
                reply_id=reply_id,
                voter_id=user_id,
                timestamp=time.time(),
            )
            return g_Voter2Reply.select().where(g_Voter2Reply.reply_id == reply_id).count()

        except:
            return False

    def delete(self, del_id):
        try:
            del_count2 = g_Voter2Reply.delete().where(g_Voter2Reply.reply_id == del_id)
            del_count2.execute()

            del_count3 = g_Post2Reply.delete().where(g_Post2Reply.reply_id == del_id)
            del_count3.execute()

            del_count4 = g_Post2Reply.delete().where(g_Post2Reply.reply_id == del_id)
            del_count4.execute()

            del_count = g_Reply.delete().where(g_Reply.uid == del_id)
            del_count.execute()

            return True
        except:

            return False


    def get_num_by_cat(self, cat_str):
        return g_Voter2Reply.select().where(g_Voter2Reply.id_cats.contains(',{0},'.format(cat_str))).count()

    def query_keywords_empty(self):
        return g_Voter2Reply.select().where(g_Voter2Reply.keywords == '')

    def query_dated(self, num=8):
        return g_Voter2Reply.select().order_by(g_Voter2Reply.time_update).limit(num)

    def query_cat_recent(self, cat_id, num=8):
        return g_Voter2Reply.select().join(g_Post2Tag).where(g_Post2Tag.tag == cat_id).order_by(
            g_Voter2Reply.time_update.desc()).limit(num)

    def query_most(self, num=8):
        return g_Voter2Reply.select().order_by(g_Voter2Reply.view_count.desc()).limit(num)

    def update_view_count(self, citiao):
        entry = g_Voter2Reply.update(view_count=g_Voter2Reply.view_count + 1).where(g_Voter2Reply.title == citiao)
        entry.execute()

    def update_view_count_by_uid(self, uid):
        entry = g_Voter2Reply.update(view_count=g_Voter2Reply.view_count + 1).where(g_Voter2Reply.uid == uid)
        entry.execute()

    def update_keywords(self, uid, inkeywords):
        entry = g_Voter2Reply.update(keywords=inkeywords).where(g_Voter2Reply.uid == uid)
        entry.execute()

    def get_by_wiki(self, citiao):
        tt = g_Voter2Reply.select().where(g_Voter2Reply.title == citiao).count()
        if tt == 0:
            return None
        else:
            self.update_view_count(citiao)
            return g_Voter2Reply.get(g_Voter2Reply.title == citiao)

    def get_next_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = g_Voter2Reply.select().where(g_Voter2Reply.time_update < current_rec.time_update).order_by(
            g_Voter2Reply.time_update.desc())
        if query.count() == 0:
            return None
        else:
            return query.get()

    def get_previous_record(self, in_uid):
        current_rec = self.get_by_id(in_uid)
        query = g_Voter2Reply.select().where(g_Voter2Reply.time_update > current_rec.time_update).order_by(
            g_Voter2Reply.time_update)
        if query.count() == 0:
            return None
        else:
            return query.get()
