# -*- coding:utf-8 -*-

import json

import tornado.escape
import tornado.web
from torcms.model.infor2label_model import MInfor2Label
from torcms.model.info_model import MInfor
from torcms.model.info_relation_model import MInforRel
from torcms.model.evaluation_model import MEvaluation
from torcms.model.category_model import MCategory

from torcms.model.usage_model import MUsage

from  config import cfg
from torcms.core import tools
from torcms.handlers.post_handler import PostHandler
from torcms.model.infor2catalog_model import MInfor2Catalog
from torcms.model.info_hist_model import MInfoHist
from torcms.core.tools import constant


class MetaHandler(PostHandler):
    def initialize(self):

        self.init()
        self.mpost = MInfor()
        self.mcat = MCategory()
        self.cats = self.mcat.query_all()
        self.mpost_hist = MInfoHist()
        self.mpost2catalog = MInfor2Catalog()
        self.mpost2label = MInfor2Label()
        self.mrel = MInforRel()

        self.musage = MUsage()
        self.mevaluation = MEvaluation()
        self.kind = '2'
        # if 'app_url_name' in cfg:
        #     self.app_url_name = cfg['app_url_name']
        # else:
        #     self.app_url_name = 'info'

    def get(self, url_str=''):

        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'cat_add':
            self.user_to_add(url_arr[1])
        elif url_arr[0] == 'catalog':
            self.catalog()
        # elif len(url_arr) == 1 and len(url_str) == 4:
        #     self.redirect('/{0}/{1}'.format(self.app_url_name, url_arr[0]))
        elif url_arr[0] == '_add':
            self.add_app()
        elif len(url_arr) == 2:
            if url_arr[0] == 'edit':
                self.to_edit_app(url_arr[1])
            elif url_arr[0] == 'add':
                self.to_add_app(url_arr[1])
            elif url_arr[0] == 'delete':
                self.to_del_app(url_arr[1])
            else:
                '''
                从相关计算中过来的。
                '''
                pass
                # self.mrel.update_relation(url_arr[1], url_arr[0])
                # self.redirect('/{0}/{1}'.format(self.app_url_name, url_arr[0]))
        else:
            kwd = {
                'title': '',
                'info': '',
            }
            self.render('html/404.html',
                        kwd=kwd,
                        userinfo=self.userinfo, )

    def post(self, url_str=''):

        url_arr = self.parse_url(url_str)

        if url_arr[0] == 'to_add':
            self.add()
        elif url_arr[0] == 'rel':
            if self.get_current_user():
                self.add_relation(url_arr[1])
            else:
                self.redirect('/user/login')
        # elif url_arr[0] == 'comment_add':
        #     self.add_comment(url_arr[1])
        elif url_arr[0] == 'edit':
            self.update(url_arr[1])
        elif url_arr[0] == 'add':
            self.add(url_arr[1])
        elif url_arr[0] == '_add':
            self.map_add()
        else:
            return False

    def catalog(self):
        self.render('infor/app/catalog.html',
                    userinfo=self.userinfo,
                    kwd={'uid': '',}
                    )

    @tornado.web.authenticated
    def user_to_add(self, catid, sig = ''):

        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        uid = sig +  tools.get_uu4d()
        while self.mpost.get_by_uid(uid):
            uid = sig + tools.get_uu4d()

        kwd = {
            'uid': uid,
            'userid': self.userinfo.user_name,
            'def_cat_uid': catid,
            'parentname': self.mcat.get_by_id(catid[:2] + '00').name,
            'catname': self.mcat.get_by_id(catid).name,
        }

        self.render('autogen/add/add_{0}.html'.format(catid),
                    userinfo=self.userinfo,
                    kwd=kwd)

    @tornado.web.authenticated
    def add_app(self):

        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False
        self.render('infor/app/add.html',
                    tag_infos=self.mcat.query_all(by_order=True, kind = constant['cate_info']),
                    userinfo=self.userinfo,

                    )

    @tornado.web.authenticated
    def to_add_app(self, uid):
        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False

        if self.mpost.get_by_uid(uid):
            # todo:
            # self.redirect('/{0}/edit/{1}'.format(self.app_url_name, uid))
            pass
        else:
            self.render('infor/app/add.html',
                        tag_infos=self.mcat.query_all(),
                        userinfo=self.userinfo,
                        kwd={'uid': uid,}
                        )

    @tornado.web.authenticated
    def to_del_app(self, uid):
        current_infor = self.mpost.get_by_uid(uid)

        if self.check_post_role(self.userinfo)['DELETE']:
            pass
        else:
            return False

        if self.mpost.delete(uid):
            self.redirect('/list/{0}'.format(current_infor.extinfo['def_cat_uid']))
        else:
            self.redirect('/info/{0}'.format(uid))

    @tornado.web.authenticated
    def to_edit_app(self, infoid):

        if self.check_post_role(self.userinfo)['EDIT']:
            pass
        else:
            return False

        rec_info = self.mpost.get_by_uid(infoid)

        if rec_info:
            pass
        else:
            self.render('html/404.html')
            return
        if 'def_cat_uid' in rec_info.extinfo:
            catid = rec_info.extinfo['def_cat_uid']
        else:
            catid = ''

        if len(catid) == 4:
            pass
        else:
            catid = ''

        kwd = {
            'def_cat_uid': catid,
            'parentname': self.mcat.get_by_id(catid[:2] + '00').name if catid != '' else '',
            'catname': self.mcat.get_by_id(catid).name if catid != '' else '',
            'parentlist': self.mcat.get_parent_list(),
            'userip': self.request.remote_ip
        }

        if cfg['site_type'] == 2:
            tmpl = 'autogen/edit/edit_{0}.html'.format(catid)
        else:
            tmpl = 'infor/app/edit.html'

        print('site_type: ', cfg['site_type'])
        print('Meta template:', tmpl)

        self.render(tmpl,
                    kwd=kwd,
                    calc_info=rec_info, # Deprecated
                    post_info=rec_info, # Deprecated
                    app_info=rec_info, # Deprecated
                    postinfo  = rec_info,
                    userinfo=self.userinfo,

                    unescape=tornado.escape.xhtml_unescape,
                    cat_enum=self.mcat.get_qian2(catid[:2], kind= self.kind + '0'),
                    tag_infos=self.mcat.query_all(by_order=True, kind = constant['cate_info']),
                    tag_infos2 = self.mcat.query_all(by_order=True, kind = constant['cate_info']),
                    app2tag_info=self.mpost2catalog.query_by_entity_uid(infoid, kind = constant['cate_info']),
                    app2label_info=self.mpost2label.get_by_id(infoid,kind = constant['tag_info'] ))

    # def check_update_role(self, current_info, post_data):
    #     #  to check if current user could update the meta
    #     if current_info.user_name == self.userinfo.user_name:
    #         return True
    #     elif self.userinfo.role[2] >= '1':
    #         return True
    #     elif 'def_cat_uid' in post_data and self.check_priv(self.userinfo, post_data['def_cat_uid'])['EDIT']:
    #         return True
    #     else:
    #         return False

    def get_def_cat_uid(self, post_data):
        # 下面两种处理方式，上面是原有的，暂时保留以保持兼容
        ext_cat_uid = {}
        if 'def_cat_uid' in post_data:
            ext_cat_uid['def_cat_uid'] = post_data['def_cat_uid']
            ext_cat_uid['def_cat_pid'] = '{0}00'.format(post_data['def_cat_uid'][:2])
        if 'gcat0' in post_data:
            ext_cat_uid['def_cat_uid'] = post_data['gcat0']
            ext_cat_uid['def_cat_pid'] = '{0}00'.format(post_data['gcat0'][:2])
        print(ext_cat_uid)
        return ext_cat_uid

    @tornado.web.authenticated
    def update(self, uid):

        if self.check_post_role(self.userinfo)['EDIT']:
            pass
        else:
            return False

        post_data = {}
        ext_dic = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)[0]

        post_data['user_name'] = self.userinfo.user_name

        current_info = self.mpost.get_by_uid(uid)


        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = current_info.valid

        ext_dic['def_uid'] = str(uid)
        print(post_data)

        ext_dic = dict(ext_dic, **self.get_def_cat_uid(post_data))

        ext_dic['def_tag_arr'] = [x.strip() for x in post_data['tags'].strip().strip(',').split(',')]
        ext_dic = self.extra_data(ext_dic, post_data)
        self.mpost_hist.insert_data(self.mpost.get_by_id(uid))

        self.mpost.modify_meta(uid,
                               post_data,
                               extinfo=ext_dic)
        self.update_catalog(uid)
        self.update_tag(uid)
        self.redirect('/info/{0}'.format(uid))

    @tornado.web.authenticated
    def map_add(self, uid='', sig = ''):

        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False

        ext_dic = {}
        post_data = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)[0]



        if uid == '':
            uid = sig + tools.get_uu4d()
            while self.mpost.get_by_uid(uid):
                uid = sig + tools.get_uu4d()
            post_data['uid'] = uid


        post_data['user_name'] = self.userinfo.user_name
        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = 1

        ext_dic['def_uid'] = ext_dic['ext_map_uid']

        ext_dic = dict(ext_dic, **self.get_def_cat_uid(post_data))

        ext_dic['def_tag_arr'] = [x.strip() for x in post_data['tags'].strip().strip(',').split(',')]
        ext_dic = self.extra_data(ext_dic, post_data)

        self.mpost.modify_meta(ext_dic['def_uid'],
                               post_data,
                               extinfo=ext_dic)
        self.update_catalog(ext_dic['def_uid'])
        self.update_tag(ext_dic['def_uid'])

        self.redirect('/info/{0}'.format(ext_dic['def_uid']))


    @tornado.web.authenticated
    def add(self, uid='', sig = ''):

        if self.check_post_role(self.userinfo)['ADD']:
            pass
        else:
            return False

        ext_dic = {}
        post_data = {}
        for key in self.request.arguments:
            if key.startswith('ext_') or key.startswith('tag_'):
                ext_dic[key] = self.get_argument(key)
            else:
                post_data[key] = self.get_arguments(key)[0]


        if uid == '':
            uid = sig + tools.get_uu4d()
            while self.mpost.get_by_uid(uid):
                uid = sig + tools.get_uu4d()
            post_data['uid'] = uid

        post_data['user_name'] = self.userinfo.user_name
        if 'valid' in post_data:
            post_data['valid'] = int(post_data['valid'])
        else:
            post_data['valid'] = 1

        ext_dic['def_uid'] = str(uid)

        ext_dic = dict(ext_dic, **self.get_def_cat_uid(post_data))

        ext_dic['def_tag_arr'] = [x.strip() for x in post_data['tags'].strip().strip(',').split(',')]
        ext_dic = self.extra_data(ext_dic, post_data)

        self.mpost.modify_meta(ext_dic['def_uid'],
                               post_data,
                               extinfo=ext_dic)
        self.update_catalog(ext_dic['def_uid'])
        self.update_tag(ext_dic['def_uid'])

        self.redirect('/info/{0}'.format(uid))

    @tornado.web.authenticated
    def extra_data(self, ext_dic, post_data):
        '''
        The additional information.
        :param post_data:
        :return: directory.
        '''
        return ext_dic

    # @tornado.web.authenticated
    # def add_comment(self, id_post):
    #     post_data = self.get_post_data()
    #     post_data['user_id'] = self.userinfo.uid
    #     post_data['user_name'] = self.userinfo.user_name
    #     # todo:
    #     comment_uid = self.mpost2reply.insert_data(post_data, id_post)
    #     if comment_uid:
    #         output = {
    #             'pinglun': comment_uid,
    #         }
    #     else:
    #         output = {
    #             'pinglun': 0,
    #         }
    #     return json.dump(output, self)

    def add_relation(self, f_uid, t_uid):
        if False == self.mpost.get_by_uid(t_uid):
            return False
        if f_uid == t_uid:
            '''
            关联其本身
            '''
            return False
        self.mrel.add_relation(f_uid, t_uid, 2)
        self.mrel.add_relation(t_uid, f_uid, 1)
        return True
