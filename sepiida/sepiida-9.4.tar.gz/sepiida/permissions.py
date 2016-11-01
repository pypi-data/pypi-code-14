import contextlib
import logging

import flask
import requests

import sepiida.routing
from sepiida.requests import privileged_session, user_session

LOGGER = logging.getLogger(__name__)

CONFIG = {
  'PAO_ROOT': None,
}
def configure(root):
    CONFIG['PAO_ROOT'] = root

class PermissionsRequestError(Exception):
    pass

class PermissionsConnectionError(Exception):
    pass

class PermissionsPaoRootError(Exception):
    pass

def _send_request(http_method, uri=None, querystring=None, payload=None, timeout=10, privileged=False):
    privileged = is_privileged() or privileged
    pao_root = CONFIG.get('PAO_ROOT')
    if not pao_root:
        raise PermissionsPaoRootError(
            "You must include a value for PAO_ROOT in your app config,"
            "such as https://pao.service, before querying the permissions system"
        )

    url = uri or '{}/permissions/'.format(pao_root)

    if querystring:
        url = '{}?{}'.format(url, querystring)

    session = privileged_session() if privileged else user_session()
    try:
        response = session.request(http_method, url, json=payload, timeout=timeout)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
        raise PermissionsConnectionError(e)

    if not response.ok:
        LOGGER.error('Error sending request %s %s with payload %s: %s %s',
            http_method,
            url,
            payload,
            response.status_code,
            response.text,
        )
        raise PermissionsRequestError(
            "Failed Request, Response: {}, {}, Payload: {}".format(response.status_code, response.text, payload)
        )
    return response

def _payload(resource, holder, right, namespace):
    return {
        'object'    : resource,
        'holder'    : holder,
        'right'     : right,
        'namespace' : namespace,
    }

def has_right(resource, right, namespace):
    permissions = search(resource=resource, right=right, namespace=namespace)
    return len(permissions) > 0

def has_any(resource=None, holder=None, right=None, namespace=None):
    permissions = search(resource, holder, right, namespace)
    return len(permissions) > 0

def get(uri=None, privileged=False):
    http_method = 'GET'
    response = _send_request(http_method, uri=uri, privileged=privileged)
    return response.json()

@contextlib.contextmanager
def always_privileged():
    is_privileged.nest += 1
    yield
    is_privileged.nest -= 1

def is_privileged():
    return is_privileged.nest > 0
is_privileged.nest = 0

def search(resource=None, holder=None, right=None, namespace=None, privileged=False):
    http_method = 'GET'
    filters = []
    if resource:
        filters.append("filter[object]={}".format(resource))
    if holder:
        filters.append("filter[holder]={}".format(holder))
    if right:
        filters.append("filter[right]={}".format(right))
    if namespace:
        filters.append("filter[namespace]={}".format(namespace))
    filters_qs = "&".join(filters)
    response = _send_request(http_method, querystring=filters_qs, privileged=privileged)
    return response.json()['resources']

def update_filters(filters, namespace, resource_name, right=None, app=None):
    """
    Update the provided filters so that permissions for the current user are enforced when querying the database
    The idea here is that pretty much all platform layers will include the ability to filter
    on a particular uuid for a resource. We enforce permissions by limiting their
    query in the database to a list of rows they are allowed to see.
    If the filter already limits to a subset of rows we take the union of the set
    they can see and the set they requested and update the filter accordingly
    This is designed to make it possible to apply filters in a single line
    """
    if is_privileged():
        LOGGER.debug("Refusing to constrain filters because we are currently in an always_privileged context")
        return filters
    app = app or flask.current_app
    permissions = search(right=right, namespace=namespace, privileged=False)
    resources = [permission['object'] for permission in permissions]
    parameters = [sepiida.routing.extract_parameters(app, 'GET', resource) for resource in resources]
    resource_uuids = {params['uuid'] for endpoint, params in parameters if endpoint == resource_name}
    requested_uuids = filters.get('uuid', None)
    common_uuids = resource_uuids.intersection(requested_uuids) if requested_uuids else resource_uuids
    filters['uuid'] = common_uuids
    return filters

def create(resource, holder, right, namespace, privileged=False):
    http_method = 'POST'
    payload = _payload(resource, holder, right, namespace)
    response = _send_request(http_method, payload=payload, privileged=privileged)
    return response.headers['Location']

def update(uri, resource, holder, right, namespace, privileged=False):
    http_method = 'PUT'
    payload = _payload(resource, holder, right, namespace)
    response = _send_request(http_method, uri=uri, payload=payload, privileged=privileged)
    assert response.status_code == 204

def delete(uri, privileged=False):
    http_method = 'DELETE'
    response = _send_request(http_method, uri=uri, privileged=privileged)
    assert response.status_code == 204

def delete_all(resource=None, holder=None, right=None, namespace=None, privileged=False):
    permissions = search(resource, holder, right, namespace)
    for permission in permissions:
        delete(permission['uri'], privileged=privileged)
