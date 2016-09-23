# -*- coding: utf-8

__author__ = 'bukun'

from torcms.model.core_tab import *

def run_init_tables():
    try:
        CabReply.create_table()
    except:
        pass

    try:
        CabPost2Reply.create_table()
    except:
        pass

    try:
        TabCatalog.create_table()
    except:
        pass

    try:
        TabApp2Reply.create_table()
    except:
        pass


    try:
        CabCatalog.create_table()
    except:
        pass

    try:
        CabMember.create_table()
    except:
        pass

    try:
        CabPage.create_table()
    except:
        pass

    try:
        CabPic.create_table()
    except:
        pass

    try:
        CabPost.create_table()
    except:
        pass

    try:
        CabPost2Catalog.create_table()
    except:
        pass
    try:
        CabWiki.create_table()
    except:
        pass

    try:
        CabPostHist.create_table()
    except:
        pass
    try:
        CabWikiHist.create_table()
    except:
        pass

    try:
        TabApp.create_table()
    except:
        pass

    try:
        TabCollect.create_table()
    except:
        pass

    try:
        TabApp2Catalog.create_table()
    except:
        pass

    try:
        TabAppRelation.create_table()
    except:
        pass

    try:
        TabEvaluation.create_table()
    except:
        pass

    try:
        TabUsage.create_table()
    except:
        pass



    try:
        CabReply.create_table()
    except:
        pass

    try:
        CabPost2Reply.create_table()
    except:
        pass

    try:
        CabPage.create_table()
    except:
        pass

    try:
        CabLink.create_table()
    except:
        pass

