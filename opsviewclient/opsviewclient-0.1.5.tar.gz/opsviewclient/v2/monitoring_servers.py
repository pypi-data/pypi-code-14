#!/usr/bin/env python
# coding: utf-8

from six.moves.urllib import parse

try:
    import simplejson as json
except ImportError:
    import json

from opsviewclient import base


class MonitoringServer(base.Resource):

    def __repr__(self):
        return '<MonitoringServer: %s>' % self.name

    def delete(self):
        return self.manager.delete(self)

    def update(self, **kwds):
        return self.manager.update(self, **kwds)


class MonitoringServerManager(base.Manager):

    resource_class = MonitoringServer

    def get(self, server):
        return self._get('/config/monitoringserver/%s' % base.get_id(server))

    def delete(self, server):
        return self._delete('/config/monitoringserver/%s' % base.get_id(server))

    def update(self, server, **kwds):
        body = server._info
        body.update(kwds)

        # Fix issue where the API returns nodes wrapped with '{"host": }' but
        # won't accept these for PUT and POST requests
        nodes = body.get('nodes')
        if nodes and any([n for n in nodes if 'host' in n]):
            # Manually added nodes
            ok_nodes = [n for n in nodes if 'host' not in n]
            # Nodes existing from API returning crap
            ok_nodes += [n['host'] for n in nodes if 'host' in n]

            body['nodes'] = ok_nodes

        return self._update('/config/monitoringserver/%s' % base.get_id(server),
                            body=body)

    def create(self, name, active=None, nodes=None, passive=None,
               ssh_forward=None):

        body = {'name': name}

        if active is not None:
            body['activated'] = base.fmt_str(active)

        if nodes is not None:
            if not isinstance(nodes, list):
                nodes = [nodes]

            body['nodes'] = [base.nameref(n) for n in nodes]

        if passive is not None:
            body['passive'] = base.fmt_str(passive)

        if ssh_forward is not None:
            body['ssh_forward'] = base.fmt_str(ssh_forward)

        return self._create('/config/monitoringserver', body=body)

    def list(self, rows='all', page=None, cols=None, order=None, search=None,
             in_use=None, kwds=None):

        qparams = {}

        if rows:
            qparams['rows'] = str(rows)
        if page:
            qparams['page'] = int(page)
        if cols:
            qparams['cols'] = str(cols)
        if order:
            qparams['order'] = str(order)
        if search:
            qparams['json_filter'] = json.dumps(search)
        if in_use is not None:
            qparams['in_use'] = 1 if in_use else 0

        if kwds:
            qparams.update(kwds)

        qparams = sorted(qparams.items(), key=lambda x: x[0])
        qstring = "?%s" % parse.urlencode(qparams) if qparams else ""

        return self._list('/config/monitoringserver%s' % qstring)
