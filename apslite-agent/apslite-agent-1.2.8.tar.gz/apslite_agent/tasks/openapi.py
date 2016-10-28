import logging
from pydoc import locate
from functools import reduce
from urllib import parse

from osaapi import OSA, Transaction
import requests

from apslite_agent.config import get_config
from apslite_agent.tasks import base

logger = logging.getLogger(__name__)


def mgetattr(obj, attr):
    return reduce(getattr, [obj] + attr.split('.'))


class OpenAPI(base.Task):
    name = 'openapi'

    def __init__(self, openapi, rest_url):
        self.openapi = openapi
        self.results = {}
        self.rest_url = rest_url.rstrip('/')

    def remove_old_oauth(self, url, headers, key, **kwargs):
        url = '{}{}'.format(self.rest_url, url)

        try:
            res = requests.get(url=url, headers=headers, verify=False)
            instances = res.json()
        except Exception as e:
            logger.error("Remove old oauth error: %s", e)
            return {'error': 'remove_old_oauth',
                    'message': 'Remove old oauth error: {}'.format(e)}

        for instance in instances:
            if 'oauth' in instance.get('aps', {}).get('auth', {})\
                    and instance['aps']['auth']['oauth'].get('key', '') == key:
                try:
                    ret = requests.request(
                        url='{}{}'.format(url, instance['aps']['id']),
                        headers=headers,
                        timeout=20,
                        **kwargs
                    )
                    if ret.status_code != 204:
                        raise Exception(ret.content)
                except Exception as e:
                    logger.error("Remove old oauth error: %s", e)
                    return {'error': 'remove_old_oauth',
                            'message': 'Remove old oauth error: {}'.format(e)}
        return {}

    def set_oauth(self, url, headers, **kwargs):
        url = '{}{}'.format(self.rest_url, url)

        try:
            res = requests.get(url=url, headers=headers, verify=False)
            instances = res.json()
            resource_id = self.results['app_instance']['application_resource_id']
        except Exception as e:
            logger.error("Remove old oauth error: %s", e)
            return {'error': 'remove_old_oauth',
                    'message': 'Remove old oauth error: {}'.format(e)}

        for instance in instances:
            if instance.get('app', {}).get('aps', {}).get('id', '') == resource_id:
                try:
                    ret = requests.request(
                        url='{}{}'.format(url, instance['aps']['id']),
                        headers=headers,
                        timeout=20,
                        **kwargs
                    )
                    if ret.status_code != 204:
                        raise Exception(ret.content)
                except Exception as e:
                    logger.error("Set oauth error: %s", e)
                    return {'error': 'oauth_error',
                            'message': 'Set oauth error: {}'.format(e)}
        return {}

    def get_application_id(self, headers):
        url = '{}/aps/2/applications/'.format(self.rest_url)

        try:
            res = requests.get(url=url, headers=headers, verify=False)
            instances = res.json()
            resource_id = self.results['app_instance']['application_resource_id']
        except Exception as e:
            logger.error("Get applications id error: %s", e)
            return None

        for instance in instances:
            if instance.get('app', {}).get('aps', {}).get('id', '') == resource_id:
                return instance['aps']['id']

        logger.error("Get applications id error")
        return None

    def get_application(self, application_id, headers):
        if not application_id:
            return application_id

        url = '{}/aps/2/applications/{}'.format(self.rest_url, application_id)

        try:
            res = requests.get(url=url, headers=headers, verify=False)
            instance = res.json()
            return instance
        except Exception as e:
            logger.error("Get applications id error: %s", e)
            return None

    def assign_users(self, url, headers, **kwargs):
        url = '{}{}'.format(self.rest_url, url)
        app = self.get_application(self.get_application_id(headers), headers)

        if not app:
            logger.error("Get application error")
            return {'error': 'get_application', 'message': 'Get application error'}

        try:
            tenant_resources = '{}/aps/2/resources/?implementing({})'.format(
                self.rest_url, app['tenant']['type'])
            res = requests.get(url=tenant_resources, headers=headers, verify=False)
            tenant = res.json()[0]
        except Exception as e:
            logger.error("Get tenant error: %s", e)
            return {'error': 'get_tenant',
                    'message': 'Get tenant error: {}'.format(e)}

        headers.update({'APS-Subscription-ID': tenant['aps']['subscription']})

        try:
            res = requests.get(url=url, headers=headers, verify=False)
            users = res.json()
        except Exception as e:
            logger.error("Get account users error: %s", e)
            return {'error': 'account_users',
                    'message': 'Get account users error: {}'.format(e)}

        for user in users:
            try:
                ret = requests.post(
                    url='{}/aps/2/resources/'.format(self.rest_url),
                    headers=headers,
                    timeout=20,
                    verify=False,
                    json={
                        'aps': {
                            'type': app['user']['type'],
                        },
                        'user': {
                            'aps': {
                                'id': user['aps']['id'],
                            }
                        }
                    }
                )

                if ret.status_code != 200:
                    raise Exception(ret.content)
            except Exception as e:
                logger.error("Assign users error: %s", e)
                return {'error': 'assign_users',
                        'message': 'Assign users error: {}'.format(e)}

        return {}

    def collect_usage(self, url, headers, **kwargs):
        app_id = self.get_application_id(headers)

        if not app_id:
            logger.error("Get application error")
            return {'error': 'get_application',
                    'message': 'Get application error'}

        try:
            res = requests.request(
                url='{}{}'.format(self.rest_url, url),
                headers=headers,
                timeout=20,
                **kwargs
            )
            periodic_resource_id = res.json()[0]['aps']['id']
        except Exception as e:
            logger.error("Get periodic task error: %s", e)
            return {'error': 'get_periodic_task',
                    'message': 'Get periodic task error: {}'.format(e)}

        path = '/aps/2/resources/{}/tasks'.format(periodic_resource_id)
        query = {'taskType': 'resourceUsage', 'appInstanceId': app_id}
        url = parse.urlunparse(parse.urlparse(self.rest_url)._replace(
            path=path, query=parse.urlencode(query)))
        try:
            res = requests.put(
                url=url,
                headers=headers,
                timeout=20,
                verify=False,
            )
            if res.status_code != 200:
                raise Exception(res.content)
        except Exception as e:
            logger.error("Collect usage error: %s", e)
            return {'error': 'collect_usage',
                    'message': 'Collect usage error: {}'.format(e)}

        return {}

    def run(self):
        self.results = self.data['results'] if 'results' in self.data else {}

        if not self.openapi:
            return self.result('Error', "Improperly configured")

        try:
            methods = self.data['methods']
        except IndexError:
            return self.result('Error', "Missing required parameter: 'methods'")

        p = OSA(**self.openapi)

        for method in methods:
            try:
                args = self.get_args(method.get('args', {}))

                logger.info("Calling OpenAPI method '%s' with arguments: %s",
                            method.get('name'),
                            args)

                if 'type' not in method or ('type' in method and method['type'] == 'openapi'):
                    def run():
                        return mgetattr(p, method['name'])(**args)

                    if method.get('transaction', True):
                        with Transaction(p):
                            ret = run()
                    else:
                        ret = run()

                elif method['type'] == 'rest':
                    # args.url for substituting parameters
                    args['url'] = '{}{}{}'.format(
                        self.rest_url, method['name'], args.get('url', '')
                    )
                    ret = requests.request(**args).json()
                    logger.info('REST Api data: %s', ret)
                elif method['type'] == 'workaround' and hasattr(self, method['name']):
                    # workaround logic
                    ret = getattr(self, method['name'])(**args)

                if 'error' in ret or ('status' in ret and ret['status'] != 0):
                    error_message = ret['message'] if 'message' in ret else 'Error'
                    raise Exception(ret.get('error_message', error_message))

                result = ret.get('result', ret)

                self.results[method.get('id', '')] = result
                self.results['_'] = result
            except Exception as e:
                logger.exception("openapi task error")

                self.data['results'] = self.results
                return self.result('Error', str(e), self.data)

        self.results.pop('_')
        self.data['results'] = self.results

        return self.result('OK', '', self.data)

    def get_args(self, method_args):
        """
        Iterate over existing results and supplied args, substituting @N:param_name
        with actual parameter value from Nth result.
        """

        args = {}

        for arg, value in method_args.items():
            if isinstance(value, list):
                new_value = []
                for item in value:
                    if isinstance(item, dict):
                        item = self.get_args(item)
                    new_value.append(item)
                args[arg] = new_value
            elif isinstance(value, dict):
                args[arg] = self.get_args(value)
            elif isinstance(value, str) and value.startswith('@'):
                try:
                    values = value[1:].split(':')
                    _type = None
                    if len(values) == 2:
                        rid, key = values
                    else:
                        rid, key, _type = values

                    args[arg] = reduce(lambda val, k: val[k],
                                       key.split('.'),
                                       self.results[rid])
                    if _type:
                        args[arg] = locate(_type)(args[arg])

                except Exception:
                    logger.warn("Skipping parameter that looks like a reference, but is badly "
                                "formatted: '%s'",
                                value)
                    args[arg] = value
            else:
                args[arg] = value

        return args


def task_factory(**kwargs):
    c = get_config()
    openapi = c.get('oa', {}).get('openapi', {})
    rest_url = c.get('oa', {}).get('rest_url', '')

    return {
        OpenAPI.name: OpenAPI(openapi, rest_url)
    }
