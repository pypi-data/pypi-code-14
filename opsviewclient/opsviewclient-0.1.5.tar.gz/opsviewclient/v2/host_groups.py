#!/usr/bin/env python
# coding: utf-8

from six.moves.urllib import parse

try:
    import simplejson as json
except ImportError:
    import json

from opsviewclient import base


class HostGroup(base.Resource):

    def __repr__(self):
        return '<HostGroup: %s>' % self.name

    def update(self, **kwds):
        return self.manager.update(self, **kwds)

    def delete(self):
        return self.manager.delete(self)


class HostGroupManager(base.Manager):

    resource_class = HostGroup

    def get(self, group):
        return self._get('/config/hostgroup/%s' % base.get_id(group))

    def delete(self, group):
        return self._delete('/config/hostgroup/%s' % base.get_id(group))

    def update(self, group, **kwds):
        body = group._info
        body.update(kwds)
        return self._update('/config/hostgroup/%s' % base.get_id(group), body=body)

    def create(self, name, children=None, hosts=None, parent=None):
        body = {'name': name}

        if children is not None:
            if not isinstance(children, list):
                children = [children]

            body['children'] = [base.nameref(c) for c in children]

        if hosts is not None:
            if not isinstance(hosts, list):
                hosts = [hosts]

            body['hosts'] = [base.nameref(h) for h in hosts]

        if parent is not None:
            body['parent'] = base.nameref(parent)

        return self._create('/config/hostgroup', body=body)

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

        return self._list('/config/hostgroup%s' % qstring)
