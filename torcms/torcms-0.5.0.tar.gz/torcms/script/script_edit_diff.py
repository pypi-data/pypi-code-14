# -*- coding: utf-8 -*-

import config
from torcms.core import tools
from torcms.model.post_model import MPost
from torcms.model.post_hist_model import MPostHist
from difflib import HtmlDiff
from torcms.core.tool.send_email import send_mail
from config import smtp_cfg

import re
def run_edit_diff():
    email_cnt = '''<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title></title>
    <style type="text/css">
        table.diff {font-family:Courier; border:medium;}
        .diff_header {background-color:#e0e0e0}
        td.diff_header {text-align:right}
        .diff_next {background-color:#c0c0c0}
        .diff_add {background-color:#aaffaa}
        .diff_chg {background-color:#ffff77}
        .diff_sub {background-color:#ffaaaa}
    </style></head><body>'''
    mpost = MPost()
    mposthist = MPostHist()
    recent_posts = mpost.query_recent_edited( tools.timestamp() - 24 * 60 * 60)
    for recent_post in recent_posts:
        hist_recs = mposthist.query_by_postid(recent_post.uid)
        if hist_recs.count() == 0:
            continue
        else:
            print('=' * 10)

            print(recent_post.title)
            hist_rec = hist_recs.get()

            raw_title = hist_rec.title
            new_title = recent_post.title

            test = HtmlDiff.make_file(HtmlDiff(), [raw_title], [new_title])



            # if len(test) > 1:
            start = test.find('<table class="diff"')  # 起点记录查询位置
            end = test.find('</table>')
            infobox = test[start:end] + '</table>'
            if ('diff_add' in infobox) or ('diff_chg' in infobox) or ('diff_sub' in infobox):
                email_cnt = email_cnt + '<h2 style="color:red; font-size:larger; font-weight:70;">TITLE: {0}</h2> TITLE'.format(recent_post.title) + infobox

            raw_md = hist_rec.cnt_md.split('\n')
            new_md = recent_post.cnt_md.split('\n')
            test = HtmlDiff.make_file(HtmlDiff(), raw_md, new_md)

            # if len(test) >1 :
            start = test.find('<table class="diff"')  # 起点记录查询位置
            end = test.find('</table>')

            infobox = test[start:end] + '</table>'
            if ('diff_add' in infobox) or ('diff_chg' in infobox) or ('diff_sub' in infobox):
                email_cnt = email_cnt +  '<h2 style="color:red; font-size:larger; font-weight:70;">TITLE: {0}</h2> CONTENT'.format(recent_post.title) +  infobox + '</hr>'

    email_cnt = email_cnt + '''<table class="diff" summary="Legends">
        <tr> <th colspan="2"> Legends </th> </tr>
        <tr> <td> <table border="" summary="Colors">
                      <tr><th> Colors </th> </tr>
                      <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
                      <tr><td class="diff_chg">Changed</td> </tr>
                      <tr><td class="diff_sub">Deleted</td> </tr>
                  </table></td>
             <td> <table border="" summary="Links">
                      <tr><th colspan="2"> Links </th> </tr>
                      <tr><td>(f)irst change</td> </tr>
                      <tr><td>(n)ext change</td> </tr>
                      <tr><td>(t)op</td> </tr>
                  </table></td> </tr>
    </table></body>'''

    print (email_cnt)
    send_mail(['bukun@osgeo.cn'], "{0}|{1}".format(smtp_cfg['name'], '新增文档'), email_cnt)


