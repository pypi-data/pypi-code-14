# -*- coding:utf-8 -*-

import tornado.escape
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.model.post2reply_model import MPost2Reply
from torcms.model.reply_model import MReply
from torcms.model.reply2user_model import MReply2User


class ReplyHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mreply = MReply()
        self.mreply2user = MReply2User()
        self.mpost2reply = MPost2Reply()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'get':
            self.get_by_id(url_arr[1])

    def get_by_id(self, reply_id):
        reply = self.mreply.get_reply_by_uid(reply_id)
        self.render('doc/reply/show_reply.html',
                    cnt=reply.cnt_html,
                    username=reply.user_name,
                    date=reply.date,
                    vote=reply.vote,
                    uid=reply.uid,
                    userinfo=self.userinfo,
                    unescape=tornado.escape.xhtml_unescape,
                    )
