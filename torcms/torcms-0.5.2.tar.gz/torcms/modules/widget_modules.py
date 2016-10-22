# -*- coding:utf-8 -*-

import bs4
import tornado.escape
import tornado.web
from torcms.model.post_model import MPost
from torcms.model.link_model import MLink
from torcms.model.post2catalog_model import MPost2Catalog
import config
import tornado.web
from torcms.model.category_model import MCategory
from torcms.core.tools import constant
from torcms.model.info_model import MInfor as  MInfor
from torcms.model.label_model import MPost2Label

from torcms.model.reply_model import MReply
from torcms.model.page_model import MPage
from torcms.model.rating_model import MRating

mreply = MReply()
mpage = MPage()
mrating = MRating()


class reply_panel(tornado.web.UIModule):
    def render(self, uid, userinfo):
        return self.render_string('modules/widget/reply_panel.html',
                                  uid=uid,
                                  replys=mreply.query_by_post(uid),
                                  userinfo=userinfo,
                                  unescape=tornado.escape.xhtml_unescape,
                                  linkify=tornado.escape.linkify,
                                  )


class userinfo_widget(tornado.web.UIModule, tornado.web.RequestHandler):
    def render(self, signature):
        if self.get_secure_cookie("user"):
            self.render('modules/widget/loginfo.html',
                        username=self.get_secure_cookie("user"))
        else:
            self.render('modules/widget/tologinfo.html')


class widget_editor(tornado.web.UIModule):
    def render(self, router, uid, userinfo):
        kwd = {'router': router,
               'uid': uid,
               }
        return self.render_string('modules/widget/widget_editor.html',
                                  kwd=kwd,
                                  userinfo=userinfo,
                                  )


class widget_search(tornado.web.UIModule):
    def render(self, ):
        self.mcat = MCategory()
        tag_enum = self.mcat.query_pcat(kind='20')
        return self.render_string('modules/widget/widget_search.html',
                                  cat_enum=tag_enum,
                                  tag_enum = tag_enum)


class star_rating(tornado.web.UIModule):
    def render(self, postinfo, userinfo):
        rating = False
        if userinfo:
            rating = mrating.get_rating(postinfo.uid, userinfo.uid)
        if rating:
            pass
        else:
            rating = postinfo.rating
        return self.render_string('modules/widget/star_rating.html',
                                  unescape=tornado.escape.xhtml_unescape,
                                  postinfo=postinfo,
                                  userinfo=userinfo,
                                  rating=rating,
                                  )
