'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from __future__ import unicode_literals

from typing import Iterable  # noqa

import six
from requests import Response  # noqa

from sxclient.exceptions import SXClusterNonFatalError
from sxclient.models import Cluster, QueryParameters  # noqa
from sxclient.query.cluster_session import ClusterSession  # noqa
from sxclient.query.query_handler import JSONBodyQueryHandler

from typing import Dict, Any, Type  # noqa


__all__ = [
    'OPERATION_CLASSES', 'BaseOperation', 'SingleNodeOperation',
    'VolumeNodeOperation'
]

OPERATION_CLASSES = {}  # type: Dict[str, Type[BaseOperation]]


class BaseOperationMeta(type):
    '''
    It gathers all classes that inherit from BaseOperation
    and stores them in OPERATION_CLASSES.
    '''

    def __new__(mcls, name, bases, nmspc):  # type: ignore
        if name in OPERATION_CLASSES:
            raise NameError('Operation with name %s already defined' % name)

        hidden_key = 'HIDDEN'
        hidden = nmspc.setdefault(hidden_key, False)

        cls = super(BaseOperationMeta, mcls).__new__(
            mcls, name, bases, nmspc
        )

        if not hidden:
            OPERATION_CLASSES[name] = cls

        return cls


class BaseOperation(six.with_metaclass(BaseOperationMeta, object)):  # type: ignore # noqa
    HIDDEN = True
    QUERY_HANDLER = JSONBodyQueryHandler

    def __init__(self, cluster, session):
        # type: (Cluster, ClusterSession) -> None
        self.cluster = cluster
        self.session = session

    def call(self, *args, **kwargs):
        # type: (*Any, **Any) -> Response
        return self.call_on_cluster(*args, **kwargs)

    def json_call(self, *args, **kwargs):
        # type: (*Any, **Any) -> dict
        return self.call(*args, **kwargs).json()

    def _generate_body(self, *args, **kwargs):
        # type: (*Any, **Any) -> dict
        return {}

    def _generate_query_params(self, *args, **kwargs):  # type: ignore
        raise NotImplementedError

    def _make_query(self, address, params, body):
        # type: (str, QueryParameters, dict) -> Response
        query_handler = self.QUERY_HANDLER(  # type: ignore
            address, self.cluster, self.session
        )
        query_handler.prepare_query(params, body)
        query_handler.make_query()
        return query_handler.response

    def _get_all_cluster_nodes(self):
        # type: () -> List[str]
        ListNodes = OPERATION_CLASSES['ListNodes']
        operation = ListNodes(self.cluster, self.session)
        response = operation.json_call()
        return response['nodeList']

    def call_on_node(self, address, *args, **kwargs):
        # type: (str, *Any, **Any) -> Response
        body = self._generate_body(*args, **kwargs)
        query_params = self._generate_query_params(*args, **kwargs)
        return self._make_query(address, query_params, body)

    def call_on_nodelist(self, nodes, *args, **kwargs):
        # type: (Iterable[str], *Any, **Any) -> Response
        response = None
        last_exception = None
        for node in nodes:
            try:
                response = self.call_on_node(node, *args, **kwargs)
                break
            except SXClusterNonFatalError as exc:
                last_exception = exc

        if response is None:
            assert isinstance(last_exception, BaseException)
            raise last_exception

        return response

    def call_on_cluster(self, *args, **kwargs):
        # type: (*Any, **Any) -> Response
        nodes = self._get_all_cluster_nodes()
        return self.call_on_nodelist(nodes, *args, **kwargs)


class VolumeNodeOperation(BaseOperation):
    HIDDEN = True

    def call(self, volume, *args, **kwargs):
        # type: (str, *Any, **Any) -> Response
        LocateVolume = OPERATION_CLASSES['LocateVolume']
        operation = LocateVolume(self.cluster, self.session)
        response = operation.json_call(volume)
        nodelist = response['nodeList']
        return self.call_on_nodelist(nodelist, volume, *args, **kwargs)


class SingleNodeOperation(BaseOperation):
    HIDDEN = True

    def call(self, node_address, *args, **kwargs):
        # type: (str, *Any, **Any) -> Response
        return self.call_on_node(node_address, *args, **kwargs)
