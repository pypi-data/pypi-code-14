# # -*- coding:utf-8 -*-
# import json
# import tornado.escape
# import tornado.web
# from torcms.core.base_handler import BaseHandler
# from torcms.model.post2reply_model import MPost2Reply
# from torcms.model.reply_model import MReply
# from torcms.model.reply2user_model import MReply2User
#
#
# class Post2ReplyHandler(BaseHandler):
#     def initialize(self):
#         self.init()
#         self.mreply = MReply()
#         self.mreply2user = MReply2User()
#         # self.mpost2reply = MPost2Reply()
#
#     def get(self, url_str=''):
#         url_arr = self.parse_url(url_str)
#         if url_arr[0] == 'delete':
#             self.delete(url_arr[1])
#         elif url_arr[0] == 'zan':
#             self.zan(url_arr[1])
#
#     def post(self, url_str=''):
#         url_arr = self.parse_url(url_str)
#         if url_arr[0] == 'add':
#             self.add_reply(url_arr[1])
#
#     @tornado.web.authenticated
#     def add_reply(self, id_post):
#
#         post_data = {}
#         for key in self.request.arguments:
#             post_data[key] = self.get_arguments(key)
#         post_data['user_id'] = self.userinfo.uid
#         post_data['user_name'] = self.userinfo.user_name
#
#         comment_uid = self.mreply.insert_data(post_data)
#
#         if comment_uid:
#             self.mpost2reply.insert_data(id_post, comment_uid)
#             output = {
#                 'pinglun': comment_uid,
#             }
#         else:
#             output = {
#                 'pinglun': 0,
#             }
#
#         return json.dump(output, self)
#
#     @tornado.web.authenticated
#     def zan(self, id_reply):
#         post_data = {}
#         for key in self.request.arguments:
#             post_data[key] = self.get_arguments(key)
#         post_data['user_id'] = self.userinfo.uid
#
#         # 先在外部表中更新，然后更新内部表字段的值。
#         # 有冗余，但是查看的时候避免了联合查询
#         cur_count = self.mreply2user.insert_data(self.userinfo.uid, id_reply)
#         if cur_count:
#             self.mreply.update_vote(id_reply, cur_count)
#             output = {
#                 'text_zan': cur_count,
#             }
#         else:
#             output = {
#                 'text_zan': 0,
#             }
#
#         return json.dump(output, self)
#
#     def delete(self, del_id):
#         if self.mreply2user.delete(del_id):
#             output = {
#                 'del_zan': 1
#             }
#         else:
#             output = {
#                 'del_zan': 0,
#             }
#         return json.dump(output, self)
