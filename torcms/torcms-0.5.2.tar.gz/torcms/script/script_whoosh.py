# -*- coding: UTF-8 -*-

import sys, os
import html2text
import tornado.escape

from time import sleep
import config
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

from jieba.analyse import ChineseAnalyzer

from torcms.model.post_model import MPost
from torcms.model.info_model import MInfor as MApp

from torcms.model.category_model import MCategory as  MInforCatalog

from config import router_post

mappcat = MInforCatalog()

from torcms.model.wiki_model import MWiki
from torcms.model.page_model import MPage

def do_for_app(writer, rand=True, doc_type=''):
    mpost = MApp()
    if rand:
        recs = mpost.query_random(50)
    else:
        recs = mpost.query_recent(50)

    print(recs.count())
    for rec in recs:
        # # sleep(0.1)
        text2 = rec.title + ',' + html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        # writer.update_document(path=u"/a",content="Replacement for the first document")
        writer.update_document(
                catid = '00000',
            title=rec.title,
            type=doc_type,
            link='/{0}/{1}'.format(router_post['2'], rec.uid),
            content=text2
        )


def do_for_app2(writer, rand=True):
    mpost = MApp()
    if rand:
        recs = mpost.query_random(50)
    else:
        recs = mpost.query_recent(50)

    print(recs.count())
    for rec in recs:
        # # sleep(0.1)
        text2 = rec.title + ',' + html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        # writer.update_document(path=u"/a",content="Replacement for the first document")
        catid = rec.extinfo['def_cat_uid'][:2] + '00'
        writer.update_document(
            title=rec.title,
            catid=catid,
            type='<span style="color:red;">[{0}]</span>'.format(
                mappcat.get_by_uid(rec.extinfo['def_cat_uid'][:2] + '00').name),
            link='/{0}/{1}'.format(router_post['2'], rec.uid),
            content=text2
        )


def do_for_post(writer, rand=True, doc_type=''):

    mpost = MPost()
    if rand:
        recs = mpost.query_random(50)
    else:
        recs = mpost.query_recent(50)

    print(recs.count())
    for rec in recs:
        # sleep(0.1)
        text2 = rec.title + ',' + html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        # writer.update_document(path=u"/a",content="Replacement for the first document")
        writer.update_document(
            title=rec.title,
            catid='0000',
            type=doc_type,
            link='/post/{0}.html'.format(rec.uid),
            content=text2
        )


def do_for_wiki(writer, rand=True, doc_type=''):
    mpost = MWiki()
    if rand:
        recs = mpost.query_random(50, )
    else:
        recs = mpost.query_recent(50, )

    print(recs.count())
    for rec in recs:
        # sleep(0.1)
        text2 = rec.title + ',' + html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        # writer.update_document(path=u"/a",content="Replacement for the first document")
        writer.update_document(
            title=rec.title,
            catid='0000',
            type=doc_type,
            link='/wiki/{0}'.format(rec.title),
            content=text2
        )

def do_for_page(writer, rand=True, doc_type=''):
    mpost = MPage()
    if rand:
        recs = mpost.query_random(50, )
    else:
        recs = mpost.query_recent(50, )

    print(recs.count())
    for rec in recs:
        # sleep(0.1)
        text2 = rec.title + ',' + html2text.html2text(tornado.escape.xhtml_unescape(rec.cnt_html))
        # writer.update_document(path=u"/a",content="Replacement for the first document")
        writer.update_document(
            title=rec.title,
            catid='0000',
            type=doc_type,
            link='/page/{0}.html'.format(rec.uid),
            content=text2
        )
def gen_whoosh_database(if_rand=True, kind='1', post_type={}):
    analyzer = ChineseAnalyzer()
    schema = Schema(title=TEXT(stored=True, analyzer=analyzer),
                    catid=TEXT(stored=True),
                    type=TEXT(stored=True),
                    link=ID(unique=True, stored=True, ),
                    content=TEXT(stored=True, analyzer=analyzer))
    whoosh_db = 'database/whoosh'
    if not os.path.exists(whoosh_db):
        os.makedirs(whoosh_db)
        ix = create_in(whoosh_db, schema)
    else:
        ix = open_dir(whoosh_db)

    writer = ix.writer()

    if kind == '1':
        do_for_app(writer, rand=if_rand, doc_type=post_type['info_type'])
    else:
        do_for_app2(writer, rand=if_rand)
    do_for_post(writer, rand=if_rand, doc_type=post_type['doc_type'])
    do_for_wiki(writer, rand=if_rand, doc_type=post_type['doc_type'])
    do_for_page(writer, rand=if_rand, doc_type=post_type['doc_type'])
    print('-' * 10)
    writer.commit()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        rand = False
    else:
        rand = True
    post_type = {
        'doc_type': '<span style="color:green;" class="glyphicon glyphicon-list-alt">[{0}]</span>'.format('文档'),
        'info_type': '<span style="color:blue;" class="glyphicon glyphicon-map-marker">[{0}]</span>'.format('地图'),
    }
    gen_whoosh_database(if_rand=rand, post_type=post_type)
