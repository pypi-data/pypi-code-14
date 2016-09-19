# -*- coding: utf-8 -*-#

import os
import hashlib
import cPickle
import json
import logging

from jsmin import jsmin
import scss

JS_CSS_FILE = 'hcm_cloud_js_css_file'
JS_CSS_INDEX = 'hcm_cloud_js_css_index'

"""
JsCssBaseService
provides combine,compress js,css by different target like mobile,pc
js config file like  app.json:
{
    "client": [
      "mobile",
      "pc"
    ],
    "caption": "core lib",
    "index": 5,
    "type": "js",
    "files": [
      "/static/common/start.js",
      "/static/common/common.js",
      "/static/common/controller.js",
      "/static/common/directive/directive.js",
      "/static/common/filter.js"
    ]
  }

will compress files to a single js for different target client
for example:
app.json  client is mobile and pc
"/static/common/start.js" is a js relate path
when compute mobile  find /static/common/start.js  and /static/common/start.mobile.js two files, and combine compress it
when compute pc will find /static/common/start.js and /static/common/start.pc.js two files and combine  compress it
you can define many file config like app.json

this service also cache compress lib ,you must provide cache_get(key) cachet_set(key,value)
you can define many config like app.json in one folder
config_path is your config folder path
js_path is your js file folder path js_path+'/static/common/start.js' can find your js file


css config like flex_css.json
{
    "type": "css",
    "client": [
      "pc",
      "mobile",
      "admin"
    ],
    "caption": "style lib",
    "index": 18,
    "files": [
      "/static/common/directive/directive.css",
      "/static/common/directive/templates/employee_selector.css",
      "/static/common/directive/templates/department_selector.css",
      "/static/common/components/base/base.scss"
    ]
  }


"""


class JsCssBaseService(object):
    def __init__(self, cache_get, cache_set, domain=None, cache_key_section='', js_path=None, config_path=None):
        self.cache_get = cache_get
        self.cache_set = cache_set
        self.cache_key_section = cache_key_section if cache_key_section else ''
        self.js_path = js_path
        self.config_path = config_path
        self.domain = domain if domain else 'common'

    @staticmethod
    def scss_config():
        scss.config.STATIC_ROOT = os.path.abspath(".")
        _scss = scss.Scss()
        return _scss

    def get_files_combine(self, files, client=None, is_compress=False):
        """
        get combine file by
        :param files: file list like ["/static/js/service.js","/static/js/service2.js"]
        :param client: target client name
        :param is_compress:  is need compress
        :return:
        """
        _return = ""
        for _file in files:
            fi_text = None
            path = os.path.abspath(self.js_path + _file)
            # public
            if os.path.exists(path):
                fi = open(path)
                fi_text = fi.read()
                if fi_text is not None:
                    if os.path.splitext(path)[1] == '.scss':
                        fi_text = self.scss_config().compile(fi_text)
                    _return += "\n" + fi_text
                fi.close()

            # client special
            if client is not None:
                _file_name_split = os.path.splitext(path)
                _file_name = _file_name_split[0] + '.' + client + _file_name_split[1]
                if os.path.exists(_file_name):
                    fi = open(_file_name)
                    fi_text = fi.read()
                    if fi_text is not None:
                        if os.path.splitext(_file_name)[1] == '.scss':
                            fi_text = self.scss_config().compile(fi_text)
                        _return += "\n" + fi_text
                    fi.close()
            if fi_text is None:
                logging.error("js css files not found:" + _file)
        if is_compress:
            _return = jsmin(_return)
        return _return

    def get_files_version(self, files, client=None):
        _file_combine = self.get_files_combine(files, client, False)
        sha1obj = hashlib.sha1()
        sha1obj.update(_file_combine)
        return sha1obj.hexdigest()

    def _get_index_key(self):
        """
        fetch lib index key
        :return:
        """
        return JS_CSS_INDEX + "#" + self.cache_key_section + "#" + self.domain

    def _get_lib_key(self, lib_name, client):
        """
        获取Lib的缓存Key值
        :param lib_name: lib_name like app,flex_css
        :param client: Client
        :return:
        """

        key = JS_CSS_FILE + "#" + self.cache_key_section + "#" + self.domain
        key = key + "#" + lib_name + "_" + client
        return key

    def _build_libs_index(self):
        """
        build Lib Index:seperate by client,order by index
        :return:
        """
        _index = []
        for k, v in self.get_config().items():
            for _client in v['client']:
                _index.append({
                    "name": k,
                    "client": _client,
                    "version": None,
                    "type": v['type'],
                    "index": v['index'],
                    "caption": v['caption'],
                    "amd": v.get('amd'),
                    "files": v['files']
                })
        _index.sort(key=lambda x: x['index'])
        return _index

    def get_lib(self, lib_name, client, is_debug=False):
        """
        fetch lib
        :param lib_name: Lib_name like app,flex_css
        :param client: Client
        :param is_debug: if is_debug fetch no compress lib
        :return:
        """
        if is_debug:
            _lib_config = self.get_config()[lib_name]
            _data = self.get_files_combine(_lib_config['files'], client, False)
        else:
            _lib_key = self._get_lib_key(lib_name, client)
            _data = self.get_obj(_lib_key)
            _data = '' if _data is None else _data.get('data', '')
        return _data

    def get_obj(self, key):
        _obj_s = self.cache_get(key)
        if _obj_s is None:
            return None
        else:
            try:
                return cPickle.loads(_obj_s)
            except Exception as e:
                return None

    def set_obj(self, key, obj):
        _obj_s = cPickle.dumps(obj)
        return self.cache_set(key, _obj_s)

    def get_libs_list(self, lib_type, client, debug, url_provider):
        is_debug = debug != ''
        _libs = self._build_libs_index() if is_debug else self.get_obj(self._get_index_key())
        _return = []
        for _lib in (_libs or []):
            if _lib['client'] == client and _lib['type'] == lib_type:
                _lib['src'] = ''.join([url_provider + "?lib=" + _lib['name'],
                                       "&v=" + str(_lib.get('version', '')),
                                       (("&client=" + client) if client else ""),
                                       ("&type=" + lib_type),
                                       ("&domain=" + self.domain if self.domain != 'common' else ''),
                                       ("&debug=" + debug)
                                       ])
                _return.append(_lib)
        return _return

    def build_libs(self, force=False):
        """
        build all libs
        :param force: force refresh
        :return:
        """
        _libs_index = self._build_libs_index()
        for _lib in _libs_index:
            _version = self.get_files_version(_lib['files'], _lib['client'])
            _lib_key = self._get_lib_key(_lib['name'], _lib['client'])
            _data = self.get_obj(_lib_key)
            if _data is None or _data['version'] != _version or force:
                self.set_obj(_lib_key, {
                    "version": _version,
                    "data": self.get_files_combine(_lib['files'], _lib['client'], _lib['type'] != 'css')
                })
                logging.info("build " + _lib_key + ":Version " + str(_version))
            else:
                logging.info("build " + _lib_key + ":Already Cached")
            _lib['version'] = _version
        logging.info("set key:" + self._get_index_key())
        self.set_obj(self._get_index_key(), _libs_index)

    def get_config(self):
        return self.get_common_config(self.config_path)

    @staticmethod
    def get_common_config(config_base_path):
        if not os.path.exists(config_base_path):
            return {}
        files = os.listdir(config_base_path)
        config = {}
        for f in files:
            key = os.path.splitext(f)[0]
            f = file(os.path.join(config_base_path, f))
            config[key] = json.loads(f.read())
            f.close()
        return config

    def get_libs_file_list(self, lib_type, client, debug, lib_prefix, js_prefix):
        _list = self.get_libs_list(lib_type, client, debug)
        return map(lambda x: (lib_prefix if x['name'].startswith('lib') else js_prefix) + x['src'], _list)
