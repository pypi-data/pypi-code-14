import requests
import json


class Client(object):

    def __init__(self, url, token, team):
        self.token = token
        self.team = team
        self.base_url = url

    def headers(self):
        return {
            'Authorization': 'Bearer {}'.format(
                self.token.encode('base64').strip()),
            'Content-Type': 'application/json'
        }

    def get_network_url(
            self, provider='openstack', environment='dev',
            location='cocna', pub='priv'):

        if provider == 'openstack':
            environment = 'dev'

        return (
            self.base_url +
            '/api/networks/{provider}-{environment}-{location}-{pub}'.format(
                provider=provider, location=location, pub=pub,
                environment=environment))

    def create_instance(
            self, provider, location, pub, instance_size,
            app_name, app_version, tags, env='dev'):
        instance = {}
        instance['_links'] = {}
        instance['_links']['owner'] = {'href': self.team}
        instance['_links']['network'] = {
            'href': self.get_network_url(
                provider=provider, location=location, environment=env, pub=pub)
        }

        instance['app_name'] = app_name
        instance['app_version'] = app_version
        instance['size'] = instance_size
        instance['tags'] = tags
        instance['environment'] = env

        response = requests.post(
            self.base_url + '/api/instances/', headers=self.headers(),
            data=json.dumps(instance))
        return response.status_code, json.loads(response.text)

    def delete_instance(self, instance_id):
        response = requests.delete(
            self.base_url + '/api/instances/{0}'.format(instance_id),
            headers=self.headers())
        return response.status_code, response.text

    def update_instance(self, instance_id, tags=None, size=None):

        if tags is not None:
            response = requests.put(
                self.base_url + '/api/instances/{0}'.format(instance_id),
                headers=self.headers(), data=json.dumps({'tags': tags}))

        if size is not None:
            response = requests.put(
                self.base_url + '/api/instances/{0}'.format(instance_id),
                headers=self.headers(), data=json.dumps({'size': size}))
        return response.status_code, response.text

    def get_instance(self, id=None, ip=None, detailed=False, tags=False):

        if id is None:
            return

        if ip is None:
            query = '/api/instances/{0}'.format(id)

        response = requests.get(
            self.base_url + query, headers=self.headers())

        if response.status_code >= 400:
            instance = json.loads(response.text)
            return response.status_code, instance.get('error')

        instance = json.loads(response.text)
        provider = ""
        if 'openstack' in instance:
            provider = instance.get('openstack')
        else:
            provider = instance.get('aws')

        inst_tags = instance.get('tags')
        instance_info = (
            instance.get('id'), instance.get('ip'), instance.get('app_name'),
            instance.get('location'), instance.get('size'),
            instance.get('state'))

        if detailed is True:
            instance_info = (
                '{0} \n\nProvider: \n{1} \n\nTags: \n{2} '
                '\n\nHostname: \n{3}'.format(
                    instance_info, provider, inst_tags,
                    instance.get('hostname')))
        elif tags is True:
            instance_info = '{0}'.format(inst_tags)

        return response.status_code, instance_info

    def get_instances(self, full=False, ip=None):

        if ip is not None:
            query = (
                '/api/instances/?filter=["and",'
                '["owned"],'
                '["equal", "/ip", "{ip}"]]'.format(ip=ip))
        elif full is False:
            query = '/api/instances/'
        else:
            query = '/api/instances/?filter=["and", ["true"]]'

        response = requests.get(
            self.base_url + query, headers=self.headers())

        if response.status_code >= 400:
            return response.status_code, response.json['error']

        instances = json.loads(response.text)
        instances = instances['_embedded']['instances']
        instance_info = []
        for i in instances:
                instance_info.append('{0}, {1}, {2}, {3}'.format(
                    i['id'], i['size'], i['environment'], i['state']))
        return response.status_code, instance_info
