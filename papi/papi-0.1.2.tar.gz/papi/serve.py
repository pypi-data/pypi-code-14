import logging
from papi.request import parse_request_middleware
from papi.method_override_middleware import method_override_middleware
from papi.exceptions import RestException, \
                            MalformedException, \
                            NotFoundException, \
                            MethodNotAllowedException, \
                            NotAcceptableException, \
                            ConflictException, \
                            UnsupportedMediaException, \
                            ResourceException
from traceback import format_exc
import json
import papi.fp as fp
from functools import partial
from papi.hateoas import hateoas
from papi.mime import match_mime, mime_str, parse_mime_type

logger = logging.getLogger(__name__)

def serve_resource(resource, response_writers=None):
    if isinstance(response_writers, dict):
        response_writers = response_writers.items()
    def application(environ, start_response):
        try:
            request = fp.assocs(
                        [
                            ('consumed_path', ()),
                            ('remaining_path', fp.path(['request', 'path'], environ)),
                            ('response_writers', response_writers or []),
                        ],
                        environ['request'])
            try:
                status, headers, body = handle_resource(resource, request)
            except ResourceException as e:
                e.raise_as_rest_exception()
        except RestException as e:
            status = e.get_http_status()
            status_code, status_msg = status
            headers = [('Content-type', 'text/plain;charset=utf8')]
            body = status_msg
        status_str = "{0} {1}".format(*status)
        start_response(status_str, headers)
        if type(body) is str:
            body = body.encode('utf8')
        return body
    middlewares = fp.chain(
        method_override_middleware,
        parse_request_middleware)
    return middlewares(application)

def handle_resource(resource, request, parent_resource=None):
    remaining_path = fp.prop('remaining_path', request)
    if len(remaining_path) == 0:
        return handle_resource_self(
            resource,
            request,
            parent_resource=parent_resource)
    else:
        child_name, new_request = consume_path_item(request)
        child = resource.get_child(child_name)
        return handle_resource(
            child,
            new_request,
            parent_resource=resource)

def handle_resource_self(resource, request, parent_resource):
    method = fp.prop('method', request).upper()
    if method == 'GET':
        return handle_resource_get(resource, request, parent_resource)
    elif method == 'POST':
        return handle_resource_post(resource, request, parent_resource)
    elif method == 'PUT':
        return handle_resource_put(resource, request, parent_resource)
    elif method == 'DELETE':
        return handle_resource_delete(resource, request, parent_resource)
    else:
        raise MethodNotAllowedException

def handle_resource_get(resource, request, parent_resource):
    if resource is None:
        raise NotFoundException
    accepts = fp.prop('accept', request)
    for mime_pattern in accepts:
        accepted = handle_resource_get_typed(mime_pattern, resource, request)
        if accepted is not None:
            return accepted
    raise NotAcceptableException

def handle_resource_put(resource, request, parent_resource):
    if parent_resource is None:
        raise NotFoundException
    content_type = fp.prop('content_type', request)
    path = fp.prop('consumed_path', request)
    name = fp.last(path)
    if not hasattr(parent_resource, 'store'):
        raise MethodNotAllowedException

    input = fp.prop('input',  request)
    name, body = parent_resource.store(input, name, content_type)

    return make_json_response(hateoas(path, body))

def handle_resource_delete(resource, request, parent_resource):
    if parent_resource is None:
        raise NotFoundException
    path = fp.prop('consumed_path', request)
    name = fp.last(path)
    if not hasattr(parent_resource, 'delete'):
        raise MethodNotAllowedException

    parent_resource.delete(name)

    return make_empty_response()

def handle_resource_post(resource, request, parent_resource):
    if resource is None:
        raise NotFoundException
    content_type = fp.prop('content_type', request)
    path = fp.prop('consumed_path', request)
    if not hasattr(resource, 'create'):
        raise MethodNotAllowedException

    input = fp.prop('input',  request)
    name, body = resource.create(input, content_type)

    return make_json_response(hateoas(fp.snoc(name, path), body))

def handle_resource_get_typed(mime_pattern, resource, request):
    binary_response = handle_resource_get_binary(mime_pattern, resource, request)
    if binary_response is not None:
        return binary_response
    return handle_resource_get_structured(mime_pattern, resource, request)

def handle_resource_get_binary(mime_pattern, resource, request):
    matched = resource.get_typed_body(mime_pattern)
    if matched is None:
        return None
    mime_type, body = matched
    return make_binary_response(mime_type, body)

def get_resource_digest(resource):
    try:
        digest = resource.get_structured_body(digest=True)
    except AttributeError:
        digest = resource
    return digest

def get_resource_body(resource):
    try:
        digest = resource.get_structured_body()
    except AttributeError:
        digest = resource
    return digest

def get_resource_response_writers(resource):
    try:
        response_writers = resource.get_response_writers()
    except AttributeError:
        response_writers = []
    if isinstance(response_writers, dict):
        response_writers = response_writers.items()
    return [(parse_mime_type(k), v) for k, v in response_writers]

def handle_resource_get_structured(mime_pattern, resource, request):
    raw_body = resource.get_structured_body()
    current_path = fp.prop('consumed_path', request)
    name = fp.last(current_path)

    offset = fp.path(('query', 'offset'), request)
    page = fp.path(('query', 'offset'), request) or 1
    count = fp.path(('query', 'count'), request) or 20
    if offset is None:
        offset = count * (page - 1)

    body = hateoas(current_path, raw_body)

    children = resource.get_children(offset=offset, count=count, page=page)
    if children is not None:
        children_alist = [
            (k, get_resource_digest(v)) for k, v in children
        ]

        def prepare_child(kv):
            name, value = kv
            if not isinstance(value, dict):
                value = {'_value': value}
            return fp.chain(
                    partial(fp.assoc, '_name', name),
                    partial(hateoas, fp.snoc(name, current_path))
                )(value)

        children_list = list(map(prepare_child, children_alist))
        body['_items'] = children_list
    if name is not None:
        body['_name'] = name

    response_writers = fp.concat([
        fp.prop('response_writers', request) or [],
        get_resource_response_writers(resource) or [],
        default_response_writers,
    ])
    query = fp.prop('query', request)
    for mime_type, response_writer in response_writers:
        if match_mime(mime_pattern, mime_type, ["charset"]):
            converted = response_writer(body, **query)
            return make_binary_response(mime_type, converted)

def json_writer(data, **query):
    kwargs = {}
    if query.get('pretty'):
        kwargs['indent'] = 2
    return json.dumps(data, **kwargs)

default_response_writers = [
    (parse_mime_type(k), v)
    for (k, v)
    in [
        ('text/json', json_writer),
        ('application/json', json_writer),
       ]
]

def consume_path_item(request):
    first_item = fp.head(fp.prop('remaining_path', request))
    if first_item is None:
        return None, request
    new_request = fp.chain(
        partial(
            fp.Lens.over,
            fp.prop_lens('remaining_path'),
            partial(fp.drop, 1)),
        partial(
            fp.Lens.over,
            fp.prop_lens('consumed_path'),
            partial(fp.snoc, first_item)))(request)
    return first_item, new_request

def make_json_response(
        data,
        status=200,
        headers=None):
    content_type = 'application/json'
    headers = list(headers or [])
    headers.append(('Content-type', content_type))
    body = json.dumps(data)
    if type(body) is str:
        body = body.encode('utf8')
    return ((status, status_names.get(status, 'OK')), headers, body)

def make_binary_response(
        mime_type,
        data,
        status=200,
        headers=None):
    content_type = mime_str(mime_type)
    headers = list(headers or [])
    headers.append(('Content-type', content_type))
    if type(data) is bytes:
        body = data
    else:
        body = str(data).encode('utf8')
    return ((status, status_names.get(status, 'OK')), headers, body)

def make_empty_response(mime_type=None, status=204, headers=None):
    content_type = mime_str(mime_type or parse_mime_type("text/plain"))
    headers = list(headers or [])
    headers.append(('Content-type', content_type))
    body = b""
    return ((status, status_names.get(status, 'OK')), headers, body)

status_names = {
    200: 'OK',
    201: 'Created',
    204: 'No Content'
}
