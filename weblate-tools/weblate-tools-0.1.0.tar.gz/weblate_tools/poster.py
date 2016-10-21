#-*- coding:utf-8 -*-
import requests
import cookielib
import json

# needs to be placed with cookie.txt
# login
class Poster(object):
    """docstring for Poster"""
    def __init__(self, site_url, cookie_filename):
        self.site_url = site_url
        self.session = requests.Session()
        cookiejar = cookielib.LWPCookieJar()
        cookiejar.load(cookie_filename, True, True)
        load_cookies = requests.utils.dict_from_cookiejar(cookiejar)
        self.session.cookies = requests.utils.cookiejar_from_dict(load_cookies)
        index_req = self.session.get(site_url)
        self.settings_dict = {
            "name": '', "slug": '', "project": '', "vcs": 'git', "repo": '', "push": '', "repoweb": '', 
            "git_export": '', "report_source_bugs": '', "branch": 'master', "filemask": '', "template": '', 
            "edit_template": 'on', "new_base": '', "file_format": 'po', "extra_commit_file": '', 
            "post_update_script": '', "pre_commit_script": '', "post_commit_script": '', 
            "post_push_script": '', "post_add_script": '', "allow_translation_propagation": 'on', 
            "save_history": 'on', "enable_suggestions": 'on', "suggestion_voting": 'on', 
            "suggestion_autoaccept": 3, "check_flags": '', "license": '', "license_url": '', 
            "agreement": '', "new_lang": 'contact', "merge_style": 'merge',
            "commit_message": r'Translated using Weblate (%(language_name)s),Currently translated at %(translated_percent)s%% (%(translated)s of %(total)s strings)',
            "add_message": r'Added translation using Weblate (%(language_name)s)',
            "delete_message": r'Deleted translation using Weblate (%(language_name)s)',
            "committer_name": 'gutenberg', "committer_email": 'gutenberg@indienova.com',
            "language_regex": '^[^.]+$', "_save": '', 'csrfmiddlewaretoken': ''
        }

    def post(num, project_id, comp_name, git_url, filename):
        self.session.headers['Referer'] = self.site_url + "trans/subproject/add/"
        self.settings_dict.update({
                "name": comp_name + '-' + str(num),
                "slug": comp_name.lower() + '-' + str(num),
                "project": project_id,
                "repo": git_url,
                "push": git_url,
                "filemask": 'locale/*/' + filename + '-%d.po' % num,
                'csrfmiddlewaretoken': self.session.cookies['csrftoken']
            })
        res = self.session.post(self.site_url + 'trans/subproject/add/', settings_dict)
        print  'send:' + str(num) + str(res)
        # print res.content

    def post_single(comp_name, project_id, git_url, filename):
        self.session.headers['Referer'] = self.site_url + 'trans/subproject/add/'
        self.settings_dict.update({
                "name": comp_name,
                "slug": comp_name.lower(),
                "project": project_id,
                "repo": git_url,
                "push": git_url,
                "filemask": 'locale/*/' + filename + '.po',
                'csrfmiddlewaretoken': self.session.cookies['csrftoken']
            })
        res = self.session.post(self.site_url + 'trans/subproject/add/', self.settings_dict)
        print  'send:' + str(res)
        # print res.content