# -*- coding:utf-8 -*-

import torcms.handlers.info_handler
import torcms.handlers.infocate_list_handler
import torcms.handlers.infocate_publish_handler
from torcms.handlers.admin_handler import AdminHandler
from torcms.handlers.category_handler import CategoryHandler
from torcms.handlers.entity_handler import EntityHandler
from torcms.handlers.index import IndexHandler
from torcms.handlers.info_tag_hanlder import InforTagHandler

from torcms.handlers.infocate_tag_hanler import InfoTagHandler
from torcms.handlers.post_label_handler import PostLabelHandler
from torcms.handlers.link_handler import LinkHandler, LinkAjaxHandler
from torcms.handlers.maintain_handler import MaintainCategoryHandler, MaintainCategoryAjaxHandler
from torcms.handlers.maintain_info_handler import MaintainPycateCategoryHandler
from torcms.handlers.meta_handler import MetaHandler
from torcms.handlers.page_handler import PageHandler, PageAjaxHandler
# from torcms.handlers.post2reply_handler import Post2ReplyHandler
from torcms.handlers.post_handler import PostHandler, PostAjaxHandler
from torcms.handlers.reply_handler import ReplyHandler
from torcms.handlers.search_handler import SearchHandler
from torcms.handlers.user_handler import UserHandler, UserAjaxHandler
# from torcms.handlers.widget_handler import WidgetHandler
from torcms.handlers.wiki_handler import WikiHandler

from torcms.handlers.index import IndexHandler as  AppIndexHandler
from torcms.handlers.user_info_list_handler import UserListHandler
# from torcms.handlers.label_hander import AppLabelHandler
# from torcms.handlers.labellist_hander import AppLabellistHandler
from torcms.handlers.collect_handler import CollectHandler
from torcms.handlers.evaluation_handler import EvaluationHandler
from torcms.handlers.post_info_relation_handler import RelHandler
# from torcms.handlers.info2reply_handler import Info2ReplyHandler

from torcms.handlers.post_manager import PostManHandler
from torcms.handlers.wiki_manager import WikiManHandler
from torcms.handlers.rating_handler import RatingHandler

urls = [
    ('/_rating/(.*)', RatingHandler, dict()),
    ('/post_man/(.*)', PostManHandler, dict()),
    ('/meta_man/(.*)', PostManHandler, dict()),
    ('/wiki_man/(.*)', WikiManHandler, dict()),
    ('/page_man/(.*)', WikiManHandler, dict()),
    ("/label/(.*)", PostLabelHandler, dict()),
    ("/admin/(.*)", AdminHandler, dict()),
    ("/entry/(.*)", EntityHandler, dict()),
    ("/entity/(.*)", EntityHandler, dict()),
    ("/category/(.*)", CategoryHandler, dict()),
    ("/user/p/(.*)", UserAjaxHandler, dict()),
    ("/user/(.*)", UserHandler, dict()),
    ("/post/p/(.*)", PostAjaxHandler, dict()),
    ("/post/(.*)", PostHandler, dict()),

    ("/maintain/p/category/(.*)", MaintainCategoryAjaxHandler, dict()),
    ("/maintain/category/(.*)", MaintainCategoryHandler, dict()),
    ("/link/p/(.*)", LinkAjaxHandler, dict()),
    ("/link/(.*)", LinkHandler, dict()),

    ("/page/p/(.*)", PageAjaxHandler, dict()),
    ("/page/(.*)", PageHandler, dict()),
    ("/wiki/(.*)", WikiHandler, dict()),
    ("/search/(.*)", SearchHandler, dict()),
    ("/reply/(.*)", ReplyHandler, dict()),

    # ("/widget/(.*)", WidgetHandler, dict(hinfo={})),

    ('/meta/(.*)', MetaHandler, dict()),
    # ("/info/reply/(.*)", Info2ReplyHandler, dict()),
    ("/info/(.*)", torcms.handlers.info_handler.InfoHandler, dict(hinfo={})),


    ("/maintain/claslitecategory/(.*)", MaintainPycateCategoryHandler, dict()),
    ("/list/(.*)", torcms.handlers.infocate_list_handler.InfoListHandler, dict()),
    ("/publish/(.*)", torcms.handlers.infocate_publish_handler.InfoPublishHandler, dict()),

    ("/tag/(.*)", InforTagHandler, dict()),
    ('/info_tag/(.*)', InfoTagHandler, dict(hinfo={})),

    ("/collect/(.*)", CollectHandler, dict()),
    ('/rel/(.*)', RelHandler, dict()),
    ("/user_list/(.*)", UserListHandler, dict()),

    ("/evaluate/(.*)", EvaluationHandler, dict()),
    ("/", IndexHandler, dict()),

]
