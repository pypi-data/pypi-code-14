from __future__ import unicode_literals
from coreapi.codecs import HALCodec
from . import API_ROOT
from . import utils
from . import wac_config

import wac
import simplejson as json


def configure(root_url=API_ROOT, **kwargs):
    kwargs['headers'] = {} if 'headers' not in kwargs else kwargs['headers']
    kwargs['headers']['Content-Type'] = 'application/hal+json'
    if 'error_cls' not in kwargs:
        kwargs['error_cls'] = convert_error
    root_url = wac_config.root_url if root_url is None else root_url
    wac_config.reset(root_url, **kwargs)


def convert_error(ex):
    if not hasattr(ex.response, 'data'):
        return ex
    return ResourceErrors(**ex.response.data)


class ObjectifyMixin(wac._ObjectifyMixin):
    def _objectify(self, resource_cls, **fields):
        doc = fields["hal_codec"] if "hal_codec" in fields else HALCodec().load(json.dumps(fields))
        setattr(self, 'uri', utils.to_uri(doc.url) if doc.url else "")
        [setattr(self, k, v) for k, v in doc.data.iteritems()]

        for k, v in doc.links.iteritems():
            collection_type = Resource.registry.get(k, Resource)
            lazy_uri = wac.ResourceCollection(collection_type, utils.to_uri(v.url))
            setattr(self, k, lazy_uri)


class Client(wac.Client):
    config = wac_config

    def _serialize(self, data):
        data = json.dumps(data, default=self._deserialize)
        return 'application/json', data

    def _deserialize(self, response):
        if hasattr(response, "content"):
            data = json.loads(response.content)
        elif hasattr(response, "data"):
            data = response.data
        elif len(response) == 0:
            data = list()
        else:
            data = response.__dict__.copy()
            data.pop('uri', None)
            data = dict(
                (k, v)
                for k, v in data.iteritems()
                if not isinstance(v, (Resource, type(response).collection_cls))
            )
        return data


class JSONSchemaPage(wac.Page, ObjectifyMixin):
    pass


class Resource(wac.Resource, ObjectifyMixin):
    client = Client()
    registry = wac.ResourceRegistry()

    collection_cls = wac.ResourceCollection
    page_cls = JSONSchemaPage

    def verify_on(self, verification):
        if not hasattr(self, "verifications"):
            raise NameError("NotSupportVerifyMethod")
        attrs = verification.__dict__.copy()
        return self.verifications.create(attrs)


class ResourceErrors(RuntimeError, ObjectifyMixin):
    def __init__(self, **kwargs):
        self._objectify(self.__class__, **kwargs)
        if hasattr(self, "errors"):
            errors = []
            [errors.append(ResourceError(hal_codec=error)) for error in self.errors]
            self.errors = errors

    def __str__(self):
        return json.dumps(self, sort_keys=True, indent=2, default=lambda o: o.__dict__)


class ResourceError(Resource):
    type = "errors"
