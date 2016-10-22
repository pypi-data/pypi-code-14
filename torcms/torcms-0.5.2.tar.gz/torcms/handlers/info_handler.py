# -*- coding:utf-8 -*-

import json
import random
import tornado.escape
import tornado.web

import config
from torcms.core import tools
from torcms.core.base_handler import BaseHandler
from torcms.model.infor2label_model import MInfor2Label
from torcms.model.info_model import MInfor
from torcms.model.info_relation_model import MInforRel
# from torcms.model.info_reply_model import MInfor2Reply
from torcms.model.evaluation_model import MEvaluation
from torcms.model.category_model import MCategory
from torcms.model.usage_model import MUsage
from torcms.model.infor2catalog_model import MInfor2Catalog

import tornado.gen
import tornado.web


class InfoHandler(BaseHandler):
    def initialize(self, hinfo=''):
        self.init()
        self.mevaluation = MEvaluation()
        self.mapp2catalog = MInfor2Catalog()
        self.mapp2tag = MInfor2Label()
        self.minfo = MInfor()
        self.musage = MUsage()
        self.mcat = MCategory()
        self.mrel = MInforRel()
        # self.mreply = MInfor2Reply()
        self.kind = '2'

    def get(self, url_str=''):
        url_arr = self.parse_url(url_str)
        if len(url_arr) == 1 and len(url_str) == 4:
            self.view_info(url_str)
        else:
            kwd = {
                'title': '',
                'info': '',
            }
            self.set_status(404)
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, url_str=''):
        url_arr = self.parse_url(url_str)
        if url_arr[0] == 'rel':
            if self.get_current_user():
                self.add_relation(url_arr[1], url_arr[2])
            else:
                self.redirect('/user/login')
        elif url_arr[0] == 'comment_add':
            self.add_comment(url_arr[1])
        else:
            return False

    @tornado.web.authenticated
    def add_comment(self, id_post):
        post_data = {}
        for key in self.request.arguments:
            post_data[key] = self.get_arguments(key)
        post_data['user_id'] = self.userinfo.uid
        post_data['user_name'] = self.userinfo.user_name
        comment_uid = self.mreply.insert_data(post_data, id_post)
        if comment_uid:
            output = {
                'pinglun': comment_uid,
            }
        else:
            output = {
                'pinglun': 0,
            }
        return json.dump(output, self)


    def view_info(self, info_id):

        '''
        Render the info
        :param info_id:
        :return: Nonthing.
        '''
        postinfo = self.minfo.get_by_uid(info_id)

        if postinfo.kind == self.kind:
            pass
        else:
            return

        if postinfo:
            pass
        else:
            kwd = {
                'info': '您要找的信息不存在。',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo, )
            return False
        #
        cats = self.mapp2catalog.query_by_entity_uid(info_id, kind='20')
        cat_uid_arr = []
        for cat_rec in cats:
            cat_uid = cat_rec.tag.uid
            cat_uid_arr.append(cat_uid)
        print('info category:',  cat_uid_arr)
        replys = [] # self.mreply.get_by_id(info_id)
        rel_recs = self.mrel.get_app_relations(postinfo.uid, 0, kind = '2')
        if len(cat_uid_arr) > 0:
            rand_recs = self.minfo.query_cat_random(cat_uid_arr[0], 4 - rel_recs.count() + 4)
        else:
            rand_recs = self.minfo.query_random(4 - rel_recs.count() + 4)

        self.chuli_cookie_relation(info_id)
        cookie_str = tools.get_uuid()

        if 'def_cat_uid' in postinfo.extinfo:
            ext_catid = postinfo.extinfo['def_cat_uid']
        else:
            ext_catid = ''


        if len(ext_catid) == 4:
            pass
        else:
            ext_catid = ''
        parent_name = self.mcat.get_by_id(ext_catid[:2] + '00').name if ext_catid != '' else ''
        if ext_catid != '':
            cat_rec = self.mcat.get_by_uid(ext_catid)
            role_mask_idx = cat_rec.role_mask.index('1')
            cat_name = cat_rec.name
        else:
            role_mask_idx = 0
            cat_name = ''

        parentname = '<a href="/list/{0}">{1}</a>'.format(ext_catid[:2] + '00', parent_name)

        catname = '<a href="/list/{0}">{1}</a>'.format(ext_catid, cat_name)

        kwd = {
            'pager': '',
            'url': self.request.uri,
            'cookie_str': cookie_str,
            'daohangstr': '',
            'signature': info_id,
            'tdesc': '',
            'eval_0': self.mevaluation.app_evaluation_count(info_id, 0),
            'eval_1': self.mevaluation.app_evaluation_count(info_id, 1),
            'site_url': config.site_url,
            'login': 1 if self.get_current_user() else 0,
            'has_image': 0,
            'parentlist': self.mcat.get_parent_list(),
            'parentname': parentname,
            'catname': catname,
        }
        self.minfo.view_count_increase(info_id)
        if self.get_current_user():
            self.musage.add_or_update(self.userinfo.uid, info_id)
        self.set_cookie('user_pass', cookie_str)
        tmpl = self.ext_tmpl_name(postinfo) if self.ext_tmpl_name(postinfo) else self.get_tmpl_name(postinfo)
        print('info tmpl: ' + tmpl )
        ext_catid2 = postinfo.extinfo['def_cat_uid'] if 'def_cat_uid' in postinfo.extinfo else None


        self.render(tmpl,
                    kwd=dict(kwd, **self.extra_kwd(postinfo)),
                    calc_info=postinfo, # Deprecated
                    post_info=postinfo, # Deprecated
                    postinfo = postinfo,
                    userinfo=self.userinfo,
                    relations=rel_recs,
                    rand_recs=rand_recs,
                    unescape=tornado.escape.xhtml_unescape,
                    ad_switch=random.randint(1, 18),
                    tag_info=self.mapp2tag.get_by_id(info_id, kind = tools.constant['tag_info']),
                    recent_apps=self.musage.query_recent(self.get_current_user(), 6)[1:],
                    replys=[], # replys,
                    cat_enum=self.mcat.get_qian2(ext_catid2[:2],kind = tools.constant['cate_info']) if ext_catid else [],
                    role_mask_idx=role_mask_idx,
                    )

    def extra_kwd(self, info_rec):
        '''
        The additional information.
        :param info_rec:
        :return: directory.
        '''
        return {}

    def chuli_cookie_relation(self, app_id):
        '''
        The current Info and the Info viewed last should have some relation.
        And the last viewed Info could be found from cookie.
        :param app_id: the current app
        :return: None
        '''
        last_app_uid = self.get_secure_cookie('use_app_uid')
        if last_app_uid:
            last_app_uid = last_app_uid.decode('utf-8')
        self.set_secure_cookie('use_app_uid', app_id)
        if last_app_uid and self.minfo.get_by_uid(last_app_uid):
            self.add_relation(last_app_uid, app_id)

    def ext_tmpl_name(self, rec):
        return None

    def get_tmpl_name(self, rec):
        '''
        According to the application, each info of it's classification could has different temaplate.
        :param rec: the App record.
        :return: the temaplte path.
        '''
        if 'def_cat_uid' in rec.extinfo and rec.extinfo['def_cat_uid'] != '':
            cat_id = rec.extinfo['def_cat_uid']
        else:
            cat_id = False
        if cat_id:
            tmpl = 'autogen/view/view_{0}.html'.format(cat_id)
        else:
            tmpl = 'infor/app/show_map.html'
        return tmpl

    def add_relation(self, f_uid, t_uid):
        '''
        Add the relation. And the from and to, should have different weight.
        :param f_uid:
        :param t_uid:
        :return: return True if the relation has been succesfully added.
        '''
        if self.minfo.get_by_uid(t_uid):
            pass
        else:
            return False
        if f_uid == t_uid:
            return False

        # 针对分类进行处理。只有落入相同分类的，才加1
        f_cats = self.mapp2catalog.query_by_entity_uid(f_uid)
        t_cats = self.mapp2catalog.query_by_entity_uid(t_uid)
        flag = False

        for f_cat in f_cats:
            print(f_cat.tag)
            for t_cat in t_cats:
                print(t_cat.tag)
                if f_cat.tag == t_cat.tag:
                    flag = True
        if flag:
            pass
        else:
            return False

        self.mrel.add_relation(f_uid, t_uid, 2)
        self.mrel.add_relation(t_uid, f_uid, 1)
        return True
