# -*- coding:utf-8 -*-

import random
import torcms.model.info_model
import torcms.model.usage_model
import tornado.web
from torcms.model.infor2label_model import MInfor2Label
from torcms.model.info_model import MInfor
from torcms.model.info_relation_model import *
from torcms.model.category_model import MCategory
import torcms.model.infor2catalog_model
from torcms.model.post_model import MPost
from html2text import html2text

from torcms.core.tools import constant

cate_info = constant['cate_info']

class app_catalog_of(tornado.web.UIModule):
    def render(self, uid_with_str):
        self.mcat = MCategory()
        recs = self.mcat.query_uid_starts_with(uid_with_str, kind = cate_info)
        # return ''
        return self.render_string('infor/modules/catalog_of.html', recs=recs)


class app_user_most(tornado.web.UIModule):
    def render(self, user_name, num, with_tag=False):
        self.mcat = torcms.model.usage_model.MUsage()
        all_cats = self.mcat.query_most(user_name, num)
        kwd = {
            'with_tag': with_tag,
        }
        return self.render_string('infor/modules/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd)


class app_user_most_by_cat(tornado.web.UIModule):
    pass


class app_user_recent(tornado.web.UIModule):
    def render(self, user_name, num, with_tag=False):
        self.mcat = torcms.model.usage_model.MUsage()
        all_cats = self.mcat.query_recent(user_name, num)
        kwd = {
            'with_tag': with_tag,
        }
        return self.render_string('infor/modules/list_user_equation.html',
                                  recs=all_cats,
                                  kwd=kwd,
                                  )


class app_user_recent_by_cat(tornado.web.UIModule):
    def render(self, user_name, cat_id, num):
        self.mcat = torcms.model.usage_model.MUsage()
        all_cats = self.mcat.query_recent_by_cat(user_name, cat_id, num)
        return self.render_string('infor/modules/list_user_equation_no_catalog.html', recs=all_cats)


class app_most_used(tornado.web.UIModule):
    def render(self, num, with_tag=False):
        self.mcat = torcms.model.info_model.MInfor()
        all_cats = self.mcat.query_most(num)
        kwd = {
            'with_tag': with_tag,
        }
        return self.render_string('infor/modules/list_equation.html', recs=all_cats,
                                  kwd=kwd,
                                  )


class app_most_used_by_cat(tornado.web.UIModule):
    def render(self, num, cat_str):
        self.mcat = torcms.model.info_model.MInfor()
        all_cats = self.mcat.query_most_by_cat(num, cat_str)
        return self.render_string('infor/modules/list_equation_by_cat.html', recs=all_cats)


class app_least_use_by_cat(tornado.web.UIModule):
    def render(self, num, cat_str):
        self.mcat = torcms.model.info_model.MInfor()
        all_cats = self.mcat.query_least_by_cat(num, cat_str)
        return self.render_string('infor/modules/list_equation_by_cat.html', recs=all_cats)


class app_recent_used(tornado.web.UIModule):
    def render(self, num, with_tag=False):
        self.mcat = torcms.model.info_model.MInfor()
        all_cats = self.mcat.query_recent(num)
        kwd = {
            'with_tag': with_tag,
        }
        return self.render_string('infor/modules/list_equation.html',
                                  recs=all_cats,
                                  kwd=kwd, )


class app_random_choose(tornado.web.UIModule):
    def render(self, num):
        self.mcat = torcms.model.info_model.MInfor()
        all_cats = self.mcat.query_random(num)
        return self.render_string('infor/modules/list_equation.html', recs=all_cats)


class app_tags(tornado.web.UIModule):
    def render(self, signature):
        print('x' * 100)
        self.mapp2tag = torcms.model.infor2catalog_model.MInfor2Catalog()
        tag_infos = self.mapp2tag.query_by_entity_uid(signature, kind = cate_info)
        out_str = ''
        ii = 1
        for tag_info in tag_infos:
            tmp_str = '<a data-inline="true" href="/tag/{0}" class="tag{1}">{2}</a>'.format(tag_info.tag.slug, ii,
                                                                                            tag_info.tag.name)
            out_str += tmp_str
            ii += 1
        print(out_str)
        print('y' * 20)
        return out_str


class label_count(tornado.web.UIModule):
    def render(self, signature):
        self.mapp2tag = MInfor2Label()
        tag_infos = self.mapp2tag.query_count(signature)

        return tag_infos


class app_menu(tornado.web.UIModule):
    def render(self, limit):
        self.mcat = MCategory()
        all_cats = self.mcat.query_field_count(limit, kind = cate_info)
        kwd = {
            'cats': all_cats,
        }
        return self.render_string('infor/modules/app_menu.html', kwd=kwd)


class baidu_search(tornado.web.UIModule):
    def render(self, ):
        baidu_script = '''
        <script type="text/javascript">(function(){document.write(unescape('%3Cdiv id="bdcs"%3E%3C/div%3E'));var bdcs = document.createElement('script');bdcs.type = 'text/javascript';bdcs.async = true;bdcs.src = 'http://znsv.baidu.com/customer_search/api/js?sid=17856875184698336445' + '&plate_url=' + encodeURIComponent(window.location.href) + '&t=' + Math.ceil(new Date()/3600000);var s = document.getElementsByTagName('script')[0];s.parentNode.insertBefore(bdcs, s);})();</script>
        '''
        return self.render_string('infor/modules/baidu_script.html',
                                  baidu_script=baidu_script)


class site_ad(tornado.web.UIModule):
    def render(self, ):
        ads = ['由科学家、工程师维护的云计算网站', '人算不如天算，天算不如云算',
               '由科学家、工程师维护的云计算网站', '人算不如天算，天算不如云算',
               '由科学家、工程师维护的云计算网站', '人算不如天算，天算不如云算',
               '由科学家、工程师维护的云计算网站', '人算不如天算，天算不如云算',
               '坚持创新，每天都在改进']
        ad = random.choice(ads)
        return self.render_string('infor/modules/site_ad.html',
                                  ad=ad)


class widget_search(tornado.web.UIModule):
    def render(self, ):
        self.mcat = MCategory()

        return self.render_string('widget/widget_search.html', cat_enum=self.mcat.query_pcat())


class amazon_ad(tornado.web.UIModule):
    def render(self, type=1):
        # 234 * 60
        ad_type1 = ['''
        <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=42&l=ur1&category=mp3_mp4&banner=0BARY9M6XKHNS1WC2SR2&f=ifr" width="234" height="60" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>

''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=42&l=ur1&category=mp3_mp4&banner=0X4GQ4QASTF3N1V5ZXR2&f=ifr" width="234" height="60" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>

''',

                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=42&l=ur1&category=wireless&banner=08DVPWWG840G8EP9GD02&f=ifr" width="234" height="60" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''<iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=42&l=ur1&category=wireless&banner=10SQ4ZP7Y2KZCYDZGJR2&f=ifr" width="234" height="60" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>

                    ''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=42&l=ur1&category=music&banner=1P46GS1W77MGWQR1PC02&f=ifr" width="234" height="60" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=42&l=ur1&category=music&banner=066AZKNF26EC01P6VG82&f=ifr" width="234" height="60" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',

                    # 468 * 60
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=13&l=ur1&category=watch&banner=0ACE9VPF5JP8WBJYZG02&f=ifr" width="468" height="60" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',

                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=26&l=ur1&category=automotive&banner=13YKTB4W3G6CDM3NH202&f=ifr" width="468" height="60" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
'''
                    ]
        # 125 * 125
        ad_type2 = ['''
        <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=books&banner=0MFA6DBCDAHXRZRR3782&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=mp3_mp4&banner=0K8V07YRN1NWHM2KRN02&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=office&banner=04VCDRJVW3TKQT4W20R2&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>

                    ''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=office&banner=1RZ1AXKCSD4HB04KK782&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=wireless&banner=19YZYB3P74ASGMFN0W82&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=wireless&banner=0JD78B4ZJFRWPTPJBJG2&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=camera&banner=127637A0YZ289SHE4WR2&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=camera&banner=0EMZWWMZFTQ5FJ5KKN82&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
 <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=movie&banner=13EJ0J8HRV4NJEMQ4F82&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=home&banner=1BJK5SZ1AWBXD2EMHJ02&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=home&banner=1KZTFQ8AXVDGM27XVN82&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=game&banner=0ZK33A1TMFQXZFBQNJ02&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''',
                    '''
                    <iframe src="http://rcm-cn.amazon-adsystem.com/e/cm?t=yunsuan-23&o=28&p=21&l=ur1&category=food&banner=0HPWRM2EDM1HQMM68Z82&f=ifr" width="125" height="125" scrolling="no" border="0" marginwidth="0" style="border:none;" frameborder="0"></iframe>
''', ]

        if type == 1:
            uu = random.choice(ad_type1)
        else:
            uu = random.choice(ad_type2)
        kwd = {

        }
        # 暂时不添加
        # uu = ''
        # yyinfos = self.mrefresh.get_by_id(info_id)
        # return ''
        return self.render_string('infor/modules/amazon_ad.html',
                                  kwd=kwd,
                                  ad_html=uu, )


class rel_post2app(tornado.web.UIModule):
    def render(self, uid, num, ):
        self.app = MInfor()
        self.relation = MRelPost2Infor()
        kwd = {
            'app_f': 'post',
            'app_t': 'info',
            'uid': uid,
        }
        rel_recs = self.relation.get_app_relations(uid, num)

        rand_recs = self.app.query_random(num - rel_recs.count() + 2)

        return self.render_string('infor/modules/relation_post2app.html',
                                  relations=rel_recs,
                                  rand_recs=rand_recs,
                                  kwd=kwd, )


class rel_app2post(tornado.web.UIModule):
    def render(self, uid, num, ):
        self.mpost = MPost()
        self.relation = MRelInfor2Post()
        kwd = {
            'app_f': 'info',
            'app_t': 'post',
            'uid': uid,
        }
        rel_recs = self.relation.get_app_relations(uid, num)

        rand_recs = self.mpost.query_random(num - rel_recs.count() + 2)

        return self.render_string('infor/modules/relation_app2post.html',
                                  relations=rel_recs,
                                  rand_recs=rand_recs,
                                  kwd=kwd, )


class ImgSlide(tornado.web.UIModule):
    def render(self, info):
        return self.render_string('infor/modules/img_slide.html', post_info=info)


class UserInfo(tornado.web.UIModule):
    def render(self, uinfo, uop):
        return self.render_string('infor/modules/user_info.html', userinfo=uinfo, userop=uop)


class VipInfo(tornado.web.UIModule):
    def render(self, uinfo, uvip):
        return self.render_string('infor/modules/vip_info.html', userinfo=uinfo, uservip=uvip)


class BannerModule(tornado.web.UIModule):
    def __init__(self, parentid=''):
        self.parentid = parentid

    def render(self):
        self.mcat = MCategory()
        parentlist = self.mcat.get_parent_list()
        kwd = {
            'parentlist': parentlist,
            'parentid': self.parentid,
        }
        return self.render_string('infor/modules/banner.html', kwd=kwd)


class BreadCrumb(tornado.web.UIModule):
    def render(self, info):
        return self.render_string('infor/modules/bread_crumb.html', info=info)


class parentname(tornado.web.UIModule):
    def render(self, info):
        return self.render_string('infor/modules/parentname.html', info=info)


class catname(tornado.web.UIModule):
    def render(self, info):
        return self.render_string('infor/modules/catname.html', info=info)


class ContactInfo(tornado.web.UIModule):
    def render(self, info):
        # ip_addr = info.extinfo['userip'][0]
        # ip_arr = ip_addr.split('.')
        # if len(ip_arr) > 3:
        #     ip_arr[3] = '*'
        # maskip = '.'.join(ip_arr)
        kwd = {
            'maskip': '',  # maskip,
        }
        return self.render_string('infor/modules/contact_info.html', post_info=info, kwd=kwd)


class BreadcrumbPublish(tornado.web.UIModule):
    def render(self, sig=0):
        kwd = {
            'sig': sig,
        }
        return self.render_string('infor/modules/breadcrumb_publish.html', kwd=kwd)


class InfoList:
    def renderit(self, info=''):
        zhiding_str = ''
        tuiguang_str = ''
        imgname = 'fixed/zhanwei.png'
        if len(info.extinfo['mymps_img']) > 0:
            imgname = info.extinfo['mymps_img'][0]
        if info.extinfo['def_zhiding'] == 1:
            zhiding_str = '<span class="red">（已置顶）</span>'
        if info.extinfo['def_tuiguang'] == 1:
            tuiguang_str = '<span class="red">（已推广）</span>'

        list_type = info.extinfo['catid']

        kwd = {
            'imgname': imgname,
            'zhiding': zhiding_str,
            'tuiguan': tuiguang_str,
        }

        return self.render_string('infor/infolist/infolist_{0}.html'.format(list_type),
                                  kwd=kwd,
                                  html2text=html2text,
                                  post_info=info)
