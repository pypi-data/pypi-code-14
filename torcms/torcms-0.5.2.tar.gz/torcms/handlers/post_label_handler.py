# -*- coding:utf-8 -*-

import tornado.escape
import tornado.web

import config
from torcms.core.base_handler import BaseHandler
from torcms.core import tools
from torcms.model.label_model import MLabel
from torcms.model.label_model import MPost2Label
from torcms.model.post_model import MPost


class PostLabelHandler(BaseHandler):
    def initialize(self):
        self.init()
        self.mequa = MPost()
        self.mtag = MLabel()
        self.mapp2tag = MPost2Label()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)

        if len(url_arr) == 1:
            self.list(url_str)
        elif len(url_arr) == 2:
            self.list(url_arr[0], url_arr[1])
        else:
            return False

    def list(self, tag_slug, cur_p=''):
        '''
        根据 cat_handler.py 中的 def view_cat_new(self, cat_slug, cur_p = '')
        :param tag_slug:
        :return:
        '''
        if cur_p == '':
            current_page_number = 1
        else:
            current_page_number = int(cur_p)

        current_page_number = 1 if current_page_number < 1 else current_page_number

        pager_num = int(self.mapp2tag.total_number(tag_slug) / config.page_num)
        tag_name = ''
        kwd = {
            'tag_name': tag_name,
            'tag_slug': tag_slug,
            'title': tag_name,
            'current_page': current_page_number,

        }

        self.render('doc/label/list.html',
                    infos=self.mapp2tag.query_pager_by_slug(tag_slug, current_page_number),
                    unescape=tornado.escape.xhtml_unescape,
                    kwd=kwd,
                    userinfo=self.userinfo,
                    pager=tools.gen_pager_bootstrap_url('/label/{0}'.format(tag_slug), pager_num, current_page_number),
                    cfg=config.cfg,
                    )
