import base64
import json
import logging
import warnings

import urllib3
from dateutil.parser import parse


class DockerRegistryClient(object):
    def __init__(self, base_url, auth_realm=None, username=None, password=None):
        self._headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if auth_realm:
            self._headers.update({'Authorization': 'Basic {}'.format(auth_realm)})

        if username and password:
            pass_str = '{}:{}'.format(username, password).encode()
            auth = base64.encodebytes(pass_str).decode().replace('\n', '')
            self._headers.update({'Authorization': 'Basic {}'.format(auth)})

        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs='/etc/ssl/certs/ca-certificates.crt')
        self.base_url = base_url

    def registry_call(self, url, headers=None, method='GET'):
        if headers is None:
            headers = {}
        warnings.filterwarnings("ignore")

        headers_to_use = self._headers
        if len(headers) > 0:
            headers_to_use = self._headers.copy()
            headers_to_use.update(headers)

        # print(url, headers, method)
        response = self.http.request(method, '{}{}'.format(self.base_url, url), headers=headers_to_use)
        if 200 <= response.status < 300:
            result = {}
            if len(response.data) > 0:
                result = json.loads(response.data.decode('utf-8'))
            # print(response.data.decode('utf-8'))
            # print(response.headers)
            if response.headers.get('Docker-Content-Digest'):
                result.update({'digest': response.headers['Docker-Content-Digest']})
            return result
        else:
            print(response.status, response.data, response.headers)
            logging.error("Unable to decode json for response %s for url %s" % (response.data, url))
            raise RuntimeError(response)

    def _reorganize(self, manifest):
        dates = [json.loads(h['v1Compatibility'])['created'] for h in manifest['history']]
        dates = {parse(t).timestamp(): parse(t) for t in dates}
        return {
            'created': max(dates.items(), key=lambda x: x[0])[1],
            'tag': manifest['tag'],
            'image': manifest['name'],
            'digest': manifest['digest'],
        }

    def get_tags(self, repo):
        return self.registry_call('/v2/{}/tags/list'.format(repo))['tags']

    def get_repositories(self, ):
        return self.registry_call('/v2/_catalog')['repositories']

    def latest_ver(self, data):
        import re
        tags = [tuple(r.lstrip('v').split('.')) for r in data if re.match('v?\d+\.\d+\.\d+', r)]
        major = max(r[0] for r in tags)
        minor = max(r[1] for r in [r for r in tags if r[0] == major])
        patch = max(r[2] for r in [r for r in tags if r[0] == major and r[1] == minor])
        return '{}.{}.{}'.format(major, minor, patch)

    def get_images_with_latest_versions(self):
        return {r: self.latest_ver(self.get_tags(r)) for r in self.get_repositories()}

    def get_tag_info(self, repo, tag, **kwargs):
        return self.registry_call('/v2/{}/manifests/{}'.format(repo, tag), **kwargs)

    def delete_image(self, repo, digest, tag):
        print('deleting', repo, digest)
        h = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
        try:
            digest_v2 = self.get_tag_info(repo, tag, headers=h)['config']['digest']
            return self.registry_call('/v2/{}/manifests/{}'.format(repo, digest_v2), method='DELETE', headers=h)
        except:
            print('Deleting {}:{} ended with error'.format(repo, tag))
            pass

    def remove_old_images(self, repo, oldest_than):
        if isinstance(oldest_than, str):
            oldest_than = parse(oldest_than)
        all_tags = [self._reorganize(self.get_tag_info(repo, t)) for t in self.get_tags(repo)]
        old_tags = sorted([x for x in all_tags if x['created'] < oldest_than], key=lambda x: x['created'])
        for tag in old_tags:
            print('Deleting tag {} of {}, created at {}'.format(tag['tag'], repo, tag['created'].isoformat()))
            self.delete_image(repo, tag['digest'], tag['tag'])

    def remove_all_old_images(self, oldest_than):
        repositories = self.get_repositories()
        for repo in repositories:
            self.remove_old_images(repo, oldest_than)
