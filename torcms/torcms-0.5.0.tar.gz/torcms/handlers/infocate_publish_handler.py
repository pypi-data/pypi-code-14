# -*- coding:utf-8 -*-

import tornado
import tornado.web

from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory

class InfoPublishHandler(BaseHandler):
    def initialize(self, hinfo=''):
        self.init()
        self.minforcatalog = MCategory()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)
        if url_str == '':
            self.view_class1()
        elif len(url_str) == 4:
            self.view_class2(url_str)
        elif len(url_str) == 5:
            self.echo_class2(url_str)
        elif len(url_arr) == 2 and url_arr[1] == 'vip':
            self.view_class2(url_arr[0], 1)

    @tornado.web.authenticated
    def echo_class2(self, input=''):
        '''
        弹出的二级发布菜单
        '''
        fatherid = input[1:]
        self.write(self.format_class2(fatherid))

    @tornado.web.authenticated
    def format_class2(self, fatherid):
        dbdata = self.minforcatalog.get_qian2(fatherid[:2], kind = '20')
        outstr = '<ul class="list-group">'
        for rec in dbdata:
            if rec.uid.endswith('00'):
                continue
            role_mask_idx = rec.role_mask.index('1')
            if self.userinfo.role[role_mask_idx] >= '1':
                outstr += '''
            <a href="/meta/cat_add/{0}" class="btn btn-primary" style="display: inline-block;margin:3px;" >{1}</a>
            '''.format(rec.uid, rec.name)
        outstr += '</ul>'
        return (outstr)

    @tornado.web.authenticated
    def view_class1(self):
        dbdata = self.minforcatalog.get_parent_list( kind = '20')
        class1str = ''
        for rec in dbdata:
            role_mask_idx = rec.role_mask.index('1')
            if self.userinfo.role[role_mask_idx] >= '1':
                class1str += '''
             <a onclick="select('/publish/2{0}');" class="btn btn-primary" style="display: inline-block;margin:3px;" >{1}</a>
            '''.format(rec.uid, rec.name)

        kwd = {
            'class1str': class1str,
            'parentid': '0',
            'parentlist': self.minforcatalog.get_parent_list(),
        }
        self.render('infor/publish/publish.html',
                    userinfo=self.userinfo,
                    kwd=kwd)

    @tornado.web.authenticated
    def view_class2(self, fatherid=''):
        '''
        从第二级分类发布
        :param fatherid:
        :return:
        '''
        if self.is_admin():
            pass
        else:
            return False
        fatherid = fatherid[:2] + '00'
        kwd = {
            'class1str': self.format_class2(fatherid),
            'parentid': '0',
            'parentlist': self.minforcatalog.get_parent_list(),
        }
        self.render('infor/publish/publish2.html',
                    userinfo=self.userinfo,
                    kwd=kwd)
