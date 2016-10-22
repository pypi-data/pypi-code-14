# -*- coding:utf-8 -*-
import math

import config
import tornado.escape

from torcms.model.info_model import MInfor as  MInfor
from torcms.core.base_handler import BaseHandler
from torcms.model.category_model import MCategory

from torcms.core.torcms_redis import redisvr

from html2text import html2text

'''
关键词过滤，涉及到不同分类，使用  session 来处理。
分类下面的过滤，则使用GET的url的参数。
'''


class InfoListHandler(BaseHandler):
    def initialize(self, hinfo=''):
        self.init()
        self.template_dir_name = 'infor'
        self.minfo = MInfor()
        self.mappcat = MCategory()

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)
        print('-' * 30)
        print('infocat get url_str:', url_str)
        if len(url_str) == 4:
            self.list(url_str)
        elif len(url_str) > 4:
            self.echo_html(url_str)
        else:
            self.render('html/404.html', kwd={})

    def gen_redis_kw(self):
        condition = {}
        if self.get_current_user():
            redis_kw = redisvr.smembers(config.redis_kw + self.userinfo.user_name)
        else:
            redis_kw = []

        kw_condition_arr = []
        for x in redis_kw:
            kw_condition_arr.append(x.decode('utf-8'))
        if redis_kw:
            condition['def_tag_arr'] = kw_condition_arr
        return condition

    def echo_html(self, url_str):
        print(url_str)

        condition = self.gen_redis_kw()

        url_arr = self.parse_url(url_str)
        sig = url_arr[0]

        num = (len(url_arr) - 2) // 2

        if sig.endswith('00'):
            condition['def_cat_pid'] = sig
        else:
            condition['def_cat_uid'] = sig


        fenye_num = 1
        for ii in range(num):
            ckey = url_arr[ii * 2 + 2]

            tval = url_arr[ii * 2 + 3]
            if tval == '0':
                continue
            if ckey == 'fenye':
                # 分页参数。单独处理。
                fenye_num = int(tval)
                continue

            else:
                cval = tval
            ckey = 'tag_' + ckey
            condition[ckey] = cval

        print(condition)
        if url_arr[1] == 'con':
            infos = self.minfo.get_list_fenye(condition, fenye_num)
            self.echo_html_list_str(sig, infos)
        elif url_arr[1] == 'num':
            allinfos = self.minfo.get_list(condition)
            self.echo_html_fenye_str(allinfos.count(), fenye_num)

    def echo_html_list_str(self, list_type, infos):
        '''
        生成 list 后的 HTML 格式的字符串
        '''
        zhiding_str = ''
        tuiguang_str = ''
        imgname = 'fixed/zhanwei.png'

        kwd = {
            'imgname': imgname,
            'zhiding': zhiding_str,
            'tuiguang': tuiguang_str,
        }
        print(kwd)
        print('list type:', list_type)
        print('infos count', len(infos))
        self.render('autogen/infolist/infolist_{1}.html'.format(self.template_dir_name, list_type),
                    userinfo=self.userinfo,
                    kwd=kwd,
                    html2text=html2text,
                    unescape=tornado.escape.xhtml_unescape,
                    post_infos=infos,
                    widget_info=kwd)

    def echo_html_fenye_str(self, rec_num, fenye_num):
        '''
        生成分页的导航
        '''

        pagination_num = int(math.ceil(rec_num * 1.0 / 10))

        if pagination_num == 1 or pagination_num == 0:
            fenye_str = ''

        elif pagination_num > 1:
            pager_mid = ''
            pager_pre = ''
            pager_next = ''
            pager_last = ''
            pager_home = ''
            fenye_str = '<ul class="pagination">'

            if fenye_num > 1:
                pager_home = '''

                  <li class="{0}" name='fenye' onclick='change(this);'
                  value='{1}'><a>首页</a></li>'''.format('', 1)

                pager_pre = ''' <li class="{0}" name='fenye' onclick='change(this);'
                  value='{1}'><a>上一页</a></li>'''.format('', fenye_num - 1)
            if fenye_num > 5:
                cur_num = fenye_num - 4
            else:
                cur_num = 1

            if pagination_num > 10 and cur_num < pagination_num - 10:
                show_num = cur_num + 10

            else:
                show_num = pagination_num + 1

            for num in range(cur_num,show_num):
                if num == fenye_num:
                    checkstr = 'active'
                else:
                    checkstr = ''

                tmp_str_df = '''

                  <li class="{0}" name='fenye' onclick='change(this);'
                  value='{1}'><a>{1}</a></li>'''.format(checkstr, num)

                pager_mid += tmp_str_df
            if fenye_num < pagination_num:
                pager_next = '''

                  <li class="{0}" name='fenye' onclick='change(this);'
                  value='{1}'><a>下一页</a></li>'''.format('', fenye_num + 1)
                pager_last = '''

                  <li class="{0}" name='fenye' onclick='change(this);'
                  value='{1}'><a>末页</a></li>'''.format('', pagination_num)


            fenye_str += pager_home + pager_pre + pager_mid + pager_next + pager_last
            fenye_str += '</ul>'

        else:
            pass
        self.write(fenye_str)

    def list(self, input):
        '''
        页面打开后的渲染方法，不包含 list 的查询结果与分页导航
        '''
        print('infocat input:', input)
        condition = self.gen_redis_kw()

        sig = input
        bread_title = ''
        bread_crumb_nav_str = '<li>当前位置：<a href="/">信息</a></li>'

        if input.endswith('00'):
            parent_id = input
            parent_catname = self.mappcat.get_by_id(parent_id).name
            condition['parentid'] = [parent_id]
            catname = self.mappcat.get_by_id(sig).name
            bread_crumb_nav_str += '<li><a href="/list/{0}">{1}</a></li>'.format(sig, catname)
            bread_title = '{1}'.format(sig, catname)

        else:
            condition['catid'] = [sig]
            parent_id = sig[:2] + '00'
            parent_catname = self.mappcat.get_by_id(parent_id).name
            catname = self.mappcat.get_by_id(sig).name
            bread_crumb_nav_str += '<li><a href="/list/{0}">{1}</a></li>'.format(parent_id, parent_catname)

            bread_crumb_nav_str += '<li><a href="/list/{0}">{1}</a></li>'.format(sig, catname)
            bread_title += '{1} - '.format(parent_id, parent_catname)
            bread_title += '{1}'.format(sig, catname)

        num = self.minfo.get_num_condition(condition)

        kwd = {
            'catid': input,
            'daohangstr': bread_crumb_nav_str,
            'breadtilte': bread_title,
            'parentid': parent_id,
            'parentlist': self.mappcat.get_parent_list(),
            'condition': condition,
            'catname': catname,
            'rec_num': num,
        }

        cat_rec = self.mappcat.get_by_uid(input)
        role_mask_idx = cat_rec.role_mask.index('1')

        if self.get_current_user():
            redis_kw = redisvr.smembers(config.redis_kw + self.userinfo.user_name)
        else:
            redis_kw = []
        kw_condition_arr = []
        for x in redis_kw:
            kw_condition_arr.append(x.decode('utf-8'))
        self.render('autogen/list/list_{1}.html'.format(self.template_dir_name, input),
                    userinfo=self.userinfo,
                    kwd=kwd,
                    widget_info=kwd,
                    condition_arr=kw_condition_arr,
                    cat_enum=self.mappcat.get_qian2(parent_id[:2]),
                    role_mask_idx=role_mask_idx,

                    )
