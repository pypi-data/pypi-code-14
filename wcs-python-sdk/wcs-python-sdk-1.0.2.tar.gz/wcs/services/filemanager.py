import base64
import json
from wcs.commons.auth import Auth
from wcs.commons.config import MGR_URL
from wcs.commons.http import _post
from wcs.commons.http import _get
from wcs.commons.util import entry


class BucketManager(object):

    def __init__(self, auth):
        self.auth = auth
        self.host = MGR_URL

    def limit_check(self):
        n = 0
        while n < 1000:
            yield n
            n += 1

    def make_download_url(self, key, param):
        url = ['http://{0}/{1}'.format(self.host, key)]
        if param:
            paramlist = []
            for k, v in param.items():
                paramlist.append('{0}={1}'.format(k, v))
            paramlist = '&'.join(paramlist)
        url.append(paramlist)
        url = '?'.join(url)
        return url

    def gernerate_headers(self,url,body=None):
        token = self.auth.managertoken(url,body=body)
        headers = {'Authorization': token}
        return headers

    def download(self, key, param):
        url = self.make_down_url(key, param)
        return _get(url=url)
    
    def make_delete_url(self, bucket, key):
        return 'http://{0}/delete/{1}'.format(self.host, entry(bucket, key))

    def delete(self, bucket, key):
        url = self.make_delete_url(bucket, key)
        return _post(url=url, headers=self.gernerate_headers(url))

    def make_filestat_url(self, bucket, key):
        return 'http://{0}/stat/{1}'.format(self.host, entry(bucket, key))

    def stat(self, bucket, key):
        url = self.make_filestat_url(bucket, key)
        return  _get(url=url, headers=self.gernerate_headers(url)) 
 
    def make_list_url(self, param):
        url = ['http://{0}/list'.format(self.host)]
        if param:
            paramlist = []
            for k, v in param.items():
                paramlist.append('{0}={1}'.format(k, v))
            paramlist = '&'.join(paramlist)
        url.append(paramlist)
        url = '?'.join(url)
        return url
    
    def bucketlist(self, bucket, prefix=None, marker=None, limit=None, mode=None):
        options = {
            'bucket': bucket,
        }
        if marker is not None:
            options['marker'] = marker
        if limit is not None:
            if limit in self.limit_check():
                options['limit'] = limit
            else:
                raise ValueError("invalid limit")
        if prefix is not None:
            options['prefix'] = prefix
        if mode is not None:
            options['mode'] = mode
        url = self.make_list_url(options)
        return _get(url=url, data=options, headers=self.gernerate_headers(url))

    def fmgr_rename(self, bucket, key, key_to, force='false'):
        pass

    def params(self, params):
        if params:
            paramlist = [] 
            for k, v in params.items():
                paramlist.append('{0}={1}'.format(k, v))
            paramlist = '&'.join(paramlist) 
        return paramlist

    def move(self, fops,notifyurl=None,separate=None):
        url = 'http://{0}/fmgr/move'.format(self.host)
        data = {'fops': fops}
        if notifyurl is not None:
            data['notifyURL'] = base64.b64encode(notifyurl)
        if separate is not None:
            data['separate'] = separate
        reqdata = self.params(data)
        code, text = _post(url=url, data=reqdata,headers=self.gernerate_headers(url,body=reqdata))
        return code, text 

    def copy(self, fops, notifyurl=None, separate=None):
        url = 'http://{0}/fmgr/copy'.format(self.host)
        data = {'fops': fops}
        if notifyurl is not None:
            data['notifyURL'] = base64.b64encode(notifyurl)
        if separate is not None:
            data['separate'] = separate
        reqdata = self.params(data)
        code, text = _post(url=url, data=reqdata,headers=self.gernerate_headers(url, body=reqdata))
        return code,text 
   
    def status(self, persistentId):
        url = 'http://{0}/fmgr/status?persistentId={1}'.format(self.host, persistentId)
        return _get(url=url)
