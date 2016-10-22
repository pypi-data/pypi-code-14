# -*- coding:utf-8 -*-

import tornado.escape
import tornado.web
from torcms.core.base_handler import BaseHandler
from torcms.model.reply_model import MReply
from torcms.model.reply2user_model import MReply2User

import json

class ReplyHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.tab = MReply()
        self.mreply2user = MReply2User()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)
        if url_arr[0] == 'get':
            self.get_by_id(url_arr[1])
        elif url_arr[0] == 'list':
            self.list()
        elif url_arr[0] == 'delete':
            self.delete(url_arr[1])
        elif url_arr[0] == 'zan':
            self.zan(url_arr[1])
    def post(self,  url_str=''):
        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'add':
            self.add(url_arr[1])

    def list(self):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '单页列表',
        }
        self.render('admin/reply_ajax/reply_list.html',
                    kwd=kwd,
                    view_all=self.tab.query_all(),
                    userinfo=self.userinfo,

                    )

    def get_by_id(self, reply_id):

        reply = self.tab.get_by_uid(reply_id)
        print('get_reply:', reply_id, reply.cnt_md)

        self.render('reply/show_reply.html',
                           reply=reply,
                           username=reply.user_name,
                           date=reply.date,
                           vote=reply.vote,
                           uid=reply.uid,
                           userinfo=self.userinfo,
                           unescape=tornado.escape.xhtml_unescape,
                           )
        #
        # uu =  self.render_string('reply/show_reply.html',
        #             reply = reply,
        #             username=reply.user_name,
        #             date=reply.date,
        #             vote=reply.vote,
        #             uid=reply.uid,
        #             userinfo=self.userinfo,
        #             unescape=tornado.escape.xhtml_unescape,
        #             )
        # print('reply cnt', uu)
        # return uu
    def add(self, post_id):
        post_data = self.get_post_data()

        post_data['user_name'] = self.userinfo.user_name
        post_data['user_id'] = self.userinfo.uid
        post_data['post_id'] = post_id
        replyid  = self.tab.insert_data(post_data)
        if replyid:
            out_dic = {
                'pinglun': post_data['cnt_reply'],
                'uid': replyid
            }
            print('add reply result dic:', out_dic)
            return json.dump(out_dic, self)


    # @tornado.web.authenticated
    def zan(self, id_reply):

        print('zan', id_reply)
        # 先在外部表中更新，然后更新内部表字段的值。
        # 有冗余，但是查看的时候避免了联合查询
        self.mreply2user.insert_data(self.userinfo.uid, id_reply)
        cur_count = self.mreply2user.get_voter_count(id_reply)
        if cur_count:
            self.tab.update_vote(id_reply, cur_count)
            output = {
                'text_zan': cur_count,
            }
        else:
            output = {
                'text_zan': 0,
            }
        print('zan dic:', cur_count)

        return json.dump(output, self)

    def delete(self, del_id):
        if self.mreply2user.delete(del_id):
            output = {
                'del_zan': 1
            }
        else:
            output = {
                'del_zan': 0,
            }
        return json.dump(output, self)