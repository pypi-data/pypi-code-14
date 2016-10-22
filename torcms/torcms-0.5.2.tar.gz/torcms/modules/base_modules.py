# -*- coding:utf-8 -*-

import bs4
import tornado.escape
import tornado.web
from torcms.model.post_model import MPost
from torcms.model.link_model import MLink
from torcms.model.post2catalog_model import MPost2Catalog
import tornado.web
from torcms.model.category_model import MCategory
from torcms.core.tools import constant
from torcms.model.info_model import MInfor as  MInfor
from torcms.model.label_model import MPost2Label
from torcms.model.reply_model import MReply
from torcms.model.page_model import MPage
import config

mreply = MReply()
mpage = MPage()


class show_page(tornado.web.UIModule):
    def render(self, page_id):
        page = mpage.get_by_uid(page_id)
        if page:
            return self.render_string('modules/show_page.html',
                                      unescape=tornado.escape.xhtml_unescape,
                                      postinfo=page
                                      )
        else:
            return '<a href="/page/{0}.html">{0}</a>'.format(page_id)


class get_footer(tornado.web.UIModule):
    def render(self):
        self.mcat = MCategory()
        all_cats = self.mcat.query_all()
        kwd = {
            'cats': all_cats,
        }
        return self.render_string('modules/post/menu.html',
                                  kwd=kwd)


class previous_post_link(tornado.web.UIModule):
    def render(self, current_id):
        self.mpost = MPost()
        prev_record = self.mpost.get_previous_record(current_id)
        if prev_record is None:
            outstr = '<a>已经是最后一篇了</a>'
        else:
            outstr = '''<a href="/post/{0}.html">上一篇</a>'''.format(prev_record.uid, prev_record.title)
        return outstr


class post_most_view(tornado.web.UIModule):
    def render(self, num, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_most(num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
        }
        return self.render_string('modules/post/post_list.html', recs=recs, kwd=kwd)


class post_random(tornado.web.UIModule):
    def render(self, num, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_random(num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=recs, kwd=kwd)


class post_cat_random(tornado.web.UIModule):
    def render(self, cat_id, num, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_cat_random(cat_id, num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=recs, kwd=kwd)


class post_recent_most_view(tornado.web.UIModule):
    def render(self, num, recent, with_date=True, with_catalog=True):
        self.mpost = MPost()
        recs = self.mpost.query_recent_most(num, recent)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
        }
        return self.render_string('modules/post/post_list.html', recs=recs, kwd=kwd)


class catalog_of(tornado.web.UIModule):
    def render(self, uid_with_str):
        self.mcat = MCategory()
        recs = self.mcat.query_uid_starts_with(uid_with_str)

        return self.render_string('modules/post/catalog_of.html',
                                  recs=recs)


class post_recent(tornado.web.UIModule):
    def render(self, num=10, with_catalog=True, with_date=True):
        self.mpost = MPost()
        recs = self.mpost.query_recent(num)
        kwd = {
            'with_date': with_date,
            'with_catalog': with_catalog,
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=recs,
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd, )


class link_list(tornado.web.UIModule):
    def render(self, num=10):
        self.mlink = MLink()
        recs = self.mlink.query_link(num)
        return self.render_string('modules/post/link_list.html',
                                  recs=recs,
                                  )


class post_category_recent(tornado.web.UIModule):
    def render(self, cat_id, num=10, with_catalog=True, with_date=True):
        self.mpost = MPost()
        self.mpost2cat = MPost2Catalog()
        recs = self.mpost.query_cat_recent(cat_id, num)
        kwd = {
            'with_catalog': with_catalog,
            'with_date': with_date,
        }
        return self.render_string('modules/post/post_list.html',
                                  recs=recs,
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd, )


class showout_recent(tornado.web.UIModule):
    def render(self, cat_id, num=10, with_catalog=True, with_date=True, width=160, height=120):
        self.mpost = MPost()
        self.mpost2cat = MPost2Catalog()
        recs = self.mpost.query_cat_recent(cat_id, num)

        kwd = {
            'with_catalog': with_catalog,
            'with_date': with_date,
            'width': width,
            'height': height,
        }

        return self.render_string('modules/post/showout_list.html',
                                  recs=recs,
                                  unescape=tornado.escape.xhtml_unescape,
                                  kwd=kwd, )


class site_url(tornado.web.UIModule):
    def render(self):
        return config.site_url


class next_post_link(tornado.web.UIModule):
    def render(self, current_id):
        self.mpost = MPost()
        next_record = self.mpost.get_next_record(current_id)
        if next_record is None:
            outstr = '<a>已经是最新一篇了</a>'
        else:
            outstr = '''<a href="/post/{0}.html">下一篇</a>'''.format(next_record.uid)
        return outstr


class the_category(tornado.web.UIModule):
    def render(self, post_id):
        tmpl_str = '''<a href="/category/{0}">{1}</a>'''
        format_arr = [tmpl_str.format(uu.tag.slug, uu.tag.name) for uu in
                      MPost2Catalog().query_by_entity_uid(post_id, kind=constant['cate_post'])]
        return ', '.join(format_arr)


class list_categories(tornado.web.UIModule):
    def render(self, cat_id, list_num):
        self.mpost = MPost()
        recs = self.mpost.query_by_cat(cat_id, list_num)
        out_str = ''
        for rec in recs:
            tmp_str = '''<li><a href="/{0}">{1}</a></li>'''.format(rec.title, rec.title)
            out_str += tmp_str
        return out_str


class generate_abstract(tornado.web.UIModule):
    def render(self, html_str):
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:130] + '....'


class generate_description(tornado.web.UIModule):
    def render(self, html_str):
        tmp_str = bs4.BeautifulSoup(tornado.escape.xhtml_unescape(html_str), "html.parser")
        return tmp_str.get_text()[:100]


class category_menu(tornado.web.UIModule):
    def render(self):
        self.mcat = MCategory()
        recs = self.mcat.query_all()
        return self.render_string('modules/post/showcat_list.html',
                                  recs=recs,
                                  unescape=tornado.escape.xhtml_unescape,
                                  )


class copyright(tornado.web.UIModule):
    def render(self):
        out_str = '''<span>Build on <a href="https://github.com/bukun/TorCMS" target="_blank">TorCMS</a>.</span>'''
        return (out_str)


class post_tags(tornado.web.UIModule):
    def render(self, signature):
        self.mapp2tag = MPost2Catalog()
        tag_infos = self.mapp2tag.query_by_entity_uid(signature, kind='10')
        out_str = ''
        ii = 1
        for tag_info in tag_infos:
            tmp_str = '<a href="/category/{0}" class="tag{1}">{2}</a>'.format(tag_info.tag.slug, ii,
                                                                              tag_info.tag.name)
            out_str += tmp_str
            ii += 1
        return out_str


class ModuleCatMenu(tornado.web.UIModule):
    def render(self, with_count=True):
        self.mcat = MCategory()
        all_cats = self.mcat.query_all(by_count=True)
        kwd = {
            'cats': all_cats,
            'with_count': with_count,
        }
        return self.render_string('modules/post/menu_post.html',
                                  kwd=kwd)


class ToplineModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('modules/post/topline.html')


class baidu_share(tornado.web.UIModule):
    def render(self):
        out_str = '''<div class="bdsharebuttonbox"><a class="bds_more" href="#" data-cmd="more"></a><a title="分享到QQ空间" class="bds_qzone" href="#" data-cmd="qzone"></a><a title="分享到新浪微博" class="bds_tsina" href="#" data-cmd="tsina"></a><a title="分享到腾讯微博" class="bds_tqq" href="#" data-cmd="tqq"></a><a title="分享到人人网" class="bds_renren" href="#" data-cmd="renren"></a><a title="分享到微信" class="bds_weixin" href="#" data-cmd="weixin"></a></div>
       <script>window._bd_share_config={"common":{"bdSnsKey":{},"bdText":"","bdMini":"2","bdPic":"","bdStyle":"0","bdSize":"16"},"share":{}};with(document)0[(getElementsByTagName('head')[0]||body).appendChild(createElement('script')).src='http://bdimg.share.baidu.com/static/api/js/share.js?v=89860593.js?cdnversion='+~(-new Date()/36e5)];</script>'''
        return out_str


class catalog_pager(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        self.mpost2catalog = MPost2Catalog()
        self.mcat = MCategory()

        cat_slug = args[0]
        current = int(args[1])
        # cat_slug 分类
        # current 当前页面

        cat_rec = self.mcat.get_by_slug(cat_slug)
        num_of_cat = self.mpost2catalog.count_of_certain_category(cat_rec.uid)

        tmp_page_num = int(num_of_cat / config.page_num)

        page_num = tmp_page_num if abs(tmp_page_num - num_of_cat / config.page_num) < 0.1 else  tmp_page_num + 1

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/catalog_pager.html',
                                  kwd=kwd,
                                  cat_slug=cat_slug,
                                  pager_num=page_num,
                                  page_current=current,
                                  )


class info_label_pager(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        self.minfo = MInfor()
        tag_slug = args[0]
        current = int(args[1])

        cat_rec = self.minfo.query_by_tagname(tag_slug)

        page_num = int(cat_rec.count() / config.page_num)

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/info_label_pager.html',
                                  kwd=kwd,
                                  cat_slug=tag_slug,
                                  pager_num=page_num,
                                  page_current=current,
                                  )


class doc_label_pager(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        self.mapp2tag = MPost2Label()
        tag_slug = args[0]
        current = int(args[1])

        page_num = int(self.mapp2tag.total_number(tag_slug) / config.page_num)

        kwd = {
            'page_home': False if current <= 1 else True,
            'page_end': False if current >= page_num else True,
            'page_pre': False if current <= 1 else True,
            'page_next': False if current >= page_num else True,
        }

        return self.render_string('modules/post/doc_label_pager.html',
                                  kwd=kwd,
                                  cat_slug=tag_slug,
                                  pager_num=page_num,
                                  page_current=current,
                                  )
