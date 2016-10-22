# -*- coding:utf-8 -*-

import json

import tornado.escape
import tornado.web

import config
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.link_model import MLink


class LinkHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mlink = MLink()
        self.tmpl_dir = 'doc'
        self.tmpl_router = 'link'

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1 and url_str.endswith('.html'):
            self.wiki(url_str.split('.')[0])
        elif url_str == 'add_link':
            self.to_add_link()

        elif url_str == 'list':
            self.recent()
        elif url_str == 'refresh':
            self.refresh()

        elif url_arr[0] == 'modify':

            self.to_modify(url_arr[1])
        elif url_arr[0] == 'delete':
            self.delete(url_arr[1])

        else:
            kwd = {
                'info': '页面未找到',
            }
            self.render('html/404.html', kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, url_str=''):
        if url_str == '':
            return
        print(url_str)
        url_arr = url_str.split('/')

        if url_arr[0] == 'modify':
            self.update(url_arr[1])

        elif url_str == 'add_link':
            self.p_user_add_link()

        elif url_arr[0] == 'add_link':
            self.p_user_add_link()


        else:
            self.redirect('html/404.html')

    def recent(self):
        kwd = {
            'pager': '',
            'unescape': tornado.escape.xhtml_unescape,
            'title': '最近文档',
        }
        self.render('{1}/{0}/link_list.html'.format(self.tmpl_router,self.tmpl_dir),
                    kwd=kwd,
                    view=self.mlink.query_recent(),
                    format_date=tools.format_date,
                    userinfo=self.userinfo,
                    )

    def refresh(self):

        kwd = {
            'pager': '',
            'title': '最近文档',
        }
        self.render('doc/link/link_list.html',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    view=self.mlink.query_dated(10),
                    format_date=tools.format_date,
                    unescape=tornado.escape.xhtml_unescape, )

    def get_random(self):
        return self.mlink.query_random()

    def wiki(self, uid):
        dbdate = self.mlink.get_by_id(uid)
        if dbdate:

            self.viewit(uid)
        else:

            self.to_add(uid)

    def to_add_link(self, ):
        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        kwd = {
            'pager': '',
            'uid': '',
        }
        self.render('doc/{0}/link_add.html'.format(self.tmpl_router),
                    topmenu='',
                    kwd=kwd,
                    userinfo=self.userinfo,
                    )

    @tornado.web.authenticated
    def to_add(self, uid):
        kwd = {
            'uid': uid,
            'pager': '',
        }
        self.render('doc/{0}/link_add.html'.format(self.tmpl_router),
                    kwd=kwd,
                    )

    def __could_edit(self, uid):
        raw_data = self.mlink.get_by_id(uid)
        if not raw_data:

            return False
        if self.check_post_role(self.userinfo)['EDIT'] or raw_data.id_user == self.userinfo.user_name:
            return True
        else:
            return False

    @tornado.web.authenticated
    def update(self, uid):
        if self.__could_edit(uid):
            pass
        else:
            return False
        post_data = self.get_post_data()

        post_data['user_name'] = self.get_current_user()

        if self.tmpl_router == "link":
            self.mlink.update(uid, post_data)
            self.redirect('/link/list'.format(uid))
        else:
            if self.mlink.update(uid, post_data):
                output = {
                    'addinfo ': 1,
                }
            else:
                output = {
                    'addinfo ': 0,
                }
            return json.dump(output, self)

    @tornado.web.authenticated
    def to_modify(self, id_rec):

        # 用户具有管理权限，
        # 或
        # 文章是用户自己发布的。
        if self.__could_edit(id_rec):
            pass
        else:
            return False
        a = self.mlink.get_by_id(id_rec)

        kwd = {
            'pager': '',

        }
        self.render('doc/{0}/link_edit.html'.format(self.tmpl_router),
                    kwd=kwd,
                    unescape=tornado.escape.xhtml_unescape,
                    dbrec=a,
                    userinfo=self.userinfo,
                    )

    @tornado.web.authenticated
    def viewit(self, post_id):

        rec = self.mlink.get_by_id(post_id)

        if not rec:
            kwd = {
                'info': '您要找的分类不存在。',
            }
            self.render('html/404.html', kwd=kwd)
            return False

        kwd = {
            'pager': '',
            'editable': self.editable(),

        }

        self.render('doc/{0}/link_view.html'.format(self.tmpl_router),
                    view=rec,
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    cfg=config.cfg,
                    )

    @tornado.web.authenticated
    def p_user_add_link(self):

        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        post_data = self.get_post_data()

        post_data['user_name'] = self.get_current_user()

        cur_uid = tools.get_uudd(2)
        while self.mlink.get_by_id(cur_uid):
            cur_uid = tools.get_uudd(2)

        if self.mlink.insert_data(cur_uid, post_data):

            output = {
                'addinfo ': 1,
            }
        else:
            output = {
                'addinfo ': 0,
            }
        return json.dump(output, self)
        # self.redirect('/link/list'.format(cur_uid))

    @tornado.web.authenticated
    def user_add_link(self):

        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        post_data = self.get_post_data()


        post_data['user_name'] = self.get_current_user()

        cur_uid = tools.get_uudd(2)
        while self.mlink.get_by_id(cur_uid):
            cur_uid = tools.get_uudd(2)

        uid = self.mlink.insert_data(cur_uid, post_data)

        self.redirect('/link/list'.format(cur_uid))

    @tornado.web.authenticated
    def delete(self, del_id):
        if self.check_post_role(self.userinfo)['DELETE']:
            pass
        else:
            return False
        if self.tmpl_router == "link":

            is_deleted = self.mlink.delete(del_id)
            if is_deleted:
                self.redirect('/link/list')
            else:
                return False
        else:

            if self.mlink.delete(del_id):
                output = {
                    'del_link': 1
                }
            else:
                output = {
                    'del_link': 0,
                }
            return json.dump(output, self)


class LinkAjaxHandler(LinkHandler):
    def initialize(self):
        self.init()
        self.user_name = self.get_current_user()
        self.tmpl_dir = 'admin'
        self.tmpl_router = 'link_ajax'
        self.mlink = MLink()
